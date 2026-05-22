import json
from pathlib import Path
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from ..db.database import get_db
from ..services.ai_service import get_ai_response
from ..services.catalog_service import build_full_catalog, resolve_original_image

_BACKEND_DIR = Path(__file__).resolve().parent.parent

ALLOWED_IMAGE_HOSTS = frozenset(
    {
        "saraworldwide.com.np",
        "www.saraworldwide.com.np",
        "fbcdn.net",
        "facebook.com",
        "placehold.co",
        "www.placehold.co",
    }
)


def _is_allowed_image_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    if host in ALLOWED_IMAGE_HOSTS:
        return True
    return host.startswith("scontent") and host.endswith(".fbcdn.net")

class ChatBody(BaseModel):
    message: str

router = APIRouter()

@router.get("/info")
def get_info():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT info_key, info_value FROM company_info")
    result = {r["info_key"]: r["info_value"] for r in cur.fetchall()}
    conn.close()
    return result

def _product_store_links() -> dict[str, str]:
    """Product title -> saraworldwide.com.np permalink."""
    all_path = _BACKEND_DIR / "sara_wp_all_images.json"
    links: dict[str, str] = {}
    if not all_path.is_file():
        return links
    with open(all_path, encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        if isinstance(entry, dict) and entry.get("title") and entry.get("link"):
            links[entry["title"]] = entry["link"]
    return links


def _build_product_tree():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, parent_id FROM categories")
    cats = cur.fetchall()
    cur.execute(
        "SELECT id, category_id, name, price, image_url, benefits, effects FROM products"
    )
    prods = cur.fetchall()
    conn.close()
    store_links = _product_store_links()
    default_store = "https://saraworldwide.com.np/"
    cat_map = {c["id"]: {**c, "children": [], "products": []} for c in cats}
    cat_id_to_name = {c["id"]: c["name"] for c in cats}
    parent_of = {c["id"]: c["parent_id"] for c in cats}

    for p in prods:
        cid = p["category_id"]
        if cid not in cat_map:
            continue
        pname = p.get("name") or ""
        p["store_link"] = store_links.get(pname, default_store)
        sub_name = cat_map[cid]["name"]
        parent_id = parent_of.get(cid)
        root_name = cat_id_to_name.get(parent_id, "") if parent_id else sub_name
        original = resolve_original_image(pname, root_name, sub_name, p.get("image_url"))
        p["original_image"] = original
        if _is_generic_db_image(p.get("image_url")):
            p["image_url"] = original
        cat_map[cid]["products"].append(p)

    roots = []
    for c in cat_map.values():
        if c["parent_id"] is None:
            roots.append(c)
        else:
            pid = c["parent_id"]
            if pid in cat_map:
                cat_map[pid]["children"].append(c)
    return roots


def _is_generic_db_image(url: str | None) -> bool:
    if not url:
        return True
    u = url.strip()
    return "moringa.jpg" in u.lower() and "/2024/08/" in u


@router.get("/products")
def get_products():
    return _build_product_tree()


@router.get("/catalog")
def get_catalog():
    """Full shop catalog: DB products + gallery photos, name-matched original images."""
    try:
        roots = _build_product_tree()
    except HTTPException:
        roots = []
    return build_full_catalog(roots)

@router.get("/image-proxy")
def image_proxy(url: str):
    """Serve product images from saraworldwide.com.np (avoids hotlink/CORS issues)."""
    if not _is_allowed_image_url(url):
        raise HTTPException(status_code=400, detail="Image host not allowed")

    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            resp = client.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; SaraFoods/1.0)"},
            )
            resp.raise_for_status()
    except httpx.HTTPError as exc:
        placeholder = (
            "https://placehold.co/400x400/043d2e/ffffff?text=Product"
        )
        try:
            with httpx.Client(timeout=10, follow_redirects=True) as client:
                ph = client.get(placeholder)
                ph.raise_for_status()
                return Response(
                    content=ph.content,
                    media_type=ph.headers.get("content-type", "image/png"),
                    headers={"Cache-Control": "public, max-age=3600"},
                )
        except httpx.HTTPError:
            raise HTTPException(
                status_code=502, detail=f"Image fetch failed: {exc}"
            ) from exc

    media_type = resp.headers.get("content-type", "image/jpeg")
    return Response(
        content=resp.content,
        media_type=media_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )


def _load_all_website_images() -> list[dict]:
    """All unique saraworldwide.com.np product photos."""
    all_path = _BACKEND_DIR / "sara_wp_all_images.json"
    if all_path.is_file():
        with open(all_path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and data:
            return [
                {
                    "title": x.get("title", "Product"),
                    "url": x["url"],
                    "link": x.get("link", "https://saraworldwide.com.np/"),
                    "source": "website",
                }
                for x in data
                if isinstance(x, dict) and x.get("url")
            ]

    wp_path = _BACKEND_DIR / "sara_wp_images.json"
    if not wp_path.is_file():
        return []
    with open(wp_path, encoding="utf-8") as f:
        wp = json.load(f)
    seen: set[str] = set()
    out = []
    for title, url in wp.items():
        if url in seen:
            continue
        seen.add(url)
        out.append(
            {
                "title": title,
                "url": url,
                "link": "https://saraworldwide.com.np/",
                "source": "website",
            }
        )
    return out


@router.get("/gallery")
def get_gallery():
    """Full saraworldwide.com.np catalog photos (+ optional Facebook extras)."""
    wp_path = _BACKEND_DIR / "sara_wp_images.json"
    fb_path = _BACKEND_DIR / "sara_fb_images.json"
    wp: dict = {}
    fb: dict = {}
    if wp_path.is_file():
        with open(wp_path, encoding="utf-8") as f:
            wp = json.load(f)
    if fb_path.is_file():
        with open(fb_path, encoding="utf-8") as f:
            fb = json.load(f)

    website = _load_all_website_images()
    hero_keys = [
        "Moringa Powder",
        "Moringa Honey",
        "Virgin Coconut Oil",
        "Aloe Vera Gel",
        "Wild Honey",
        "Shilajit",
    ]
    hero = []
    seen_hero: set[str] = set()
    for k in hero_keys:
        if k in wp and wp[k] not in seen_hero:
            hero.append({"title": k, "url": wp[k], "source": "website"})
            seen_hero.add(wp[k])
    for item in website:
        if len(hero) >= 8:
            break
        if item["url"] in seen_hero:
            continue
        hero.append(item)
        seen_hero.add(item["url"])

    facebook = []
    for title, url in fb.items():
        label = title if not title.startswith("fb_image_") else "Sara Organics"
        facebook.append({"title": label, "url": url, "source": "facebook"})

    categories = {
        "food": wp.get("Moringa Powder") or wp.get("Chia Seed"),
        "beauty": wp.get("Aloe Vera Gel") or wp.get("Rose Aloe Vera Gel"),
        "spiritual": wp.get("Yarsagumba") or wp.get("Ganoderma"),
        "nursery": wp.get("Moringa Plant") or wp.get("Neem Plant"),
    }

    return {
        "hero": hero[:8],
        "website": website,
        "total_website_images": len(website),
        "facebook": facebook,
        "categories": categories,
        "links": {
            "website": "https://saraworldwide.com.np/",
            "facebook_organics": "https://www.facebook.com/saraorganics.np/",
            "facebook_main": "https://www.facebook.com/saraworldwide.com.np/",
        },
    }


@router.get("/products/stats")
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM categories WHERE parent_id IS NOT NULL")
    subs = cur.fetchone()[0]
    conn.close()
    return {"total_products": total, "total_subcategories": subs}

@router.get("/product/{name}")
def get_product(name: str):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT p.name, p.benefits, p.effects, p.price, p.image_url, "
        "c.name AS category, c.parent_id, pc.name AS root_category "
        "FROM products p "
        "JOIN categories c ON p.category_id=c.id "
        "LEFT JOIN categories pc ON c.parent_id=pc.id "
        "WHERE p.name LIKE %s LIMIT 1",
        (f"%{name}%",),
    )
    p = cur.fetchone()
    conn.close()

    store_links = _product_store_links()
    default_store = "https://saraworldwide.com.np/"

    if p:
        root_cat = p.get("root_category") or ""
        original = resolve_original_image(
            p["name"],
            root_cat,
            p.get("category") or "",
            p.get("image_url"),
        )
        p["original_image"] = original
        p["image_url"] = original
        p["store_link"] = store_links.get(p["name"], default_store)
        return p

    catalog = build_full_catalog(_build_product_tree())
    key = name.strip().lower()
    for item in catalog["products"]:
        if item["name"].strip().lower() == key:
            return {
                "name": item["name"],
                "benefits": item.get("benefits"),
                "effects": item.get("effects"),
                "price": item["price"],
                "image_url": item["original_image"],
                "original_image": item["original_image"],
                "category": item["cat"],
                "store_link": item["store_link"],
                "source": item.get("source", "gallery"),
            }

    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/chat")
def chat(body: ChatBody):
    response = get_ai_response(body.message)
    return {"response": response}


class FeedbackBody(BaseModel):
    name: str
    email: str = ""
    rating: int = 5
    message: str


@router.post("/feedback")
def submit_feedback(body: FeedbackBody):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO feedback (name, email, rating, message) VALUES (%s,%s,%s,%s)",
            (body.name, body.email, min(5, max(1, body.rating)), body.message),
        )
        conn.commit()
    finally:
        conn.close()
    return {"message": "Thank you for your feedback!"}


@router.get("/feedback")
def list_feedback():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT name, email, rating, message, created_at FROM feedback ORDER BY created_at DESC LIMIT 50"
    )
    rows = cur.fetchall()
    conn.close()
    return rows
