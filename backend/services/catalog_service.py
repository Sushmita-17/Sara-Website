"""Unified catalog: DB products + gallery photos with name-matched original images."""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..generate_product_images import (
    best_fuzzy_wp_match,
    keyword_wp_match,
    load_facebook_images,
    match_fb_image,
    match_wp_image,
)
from ..product_images import (
    DEFAULT_PRODUCT_IMAGE,
    PRODUCT_IMAGE_OVERRIDES,
    resolve_product_image_url,
)

_BACKEND = Path(__file__).resolve().parent.parent
_GENERIC_FALLBACKS = frozenset(
    {
        DEFAULT_PRODUCT_IMAGE,
        "https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg",
    }
)

_CAT_LETTERS = {
    "Category A: Food": "A",
    "Category B: Natural Cosmetics": "B",
    "Category C: Spirituals": "C",
    "Category D: Sara Nursery": "D",
}

_PHOTO_SUFFIX = re.compile(r"\s*[—–-]\s*photo\s*\d+\s*$", re.I)


def _load_wp() -> dict[str, str]:
    path = _BACKEND / "sara_wp_images.json"
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_all_website() -> list[dict]:
    path = _BACKEND / "sara_wp_all_images.json"
    if not path.is_file():
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        return []
    return [
        {
            "title": x.get("title", "Product"),
            "url": x["url"],
            "link": x.get("link", "https://saraworldwide.com.np/"),
        }
        for x in data
        if isinstance(x, dict) and x.get("url")
    ]


def _load_store_links() -> dict[str, str]:
    path = _BACKEND / "sara_wp_all_images.json"
    links: dict[str, str] = {}
    if not path.is_file():
        return links
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for entry in data:
        if not isinstance(entry, dict):
            continue
        title = entry.get("title") or ""
        link = entry.get("link")
        if title and link:
            base = gallery_base_title(title)
            links.setdefault(base, link)
            links.setdefault(title, link)
    return links


def gallery_base_title(title: str) -> str:
    return _PHOTO_SUFFIX.sub("", (title or "").strip())


def _is_generic_url(url: str | None) -> bool:
    if not url:
        return True
    u = url.strip()
    if u in _GENERIC_FALLBACKS:
        return True
    return u.endswith("/moringa.jpg") and "moringa" in u.lower()


def resolve_original_image(
    product_name: str,
    cat_name: str = "",
    sub_name: str = "",
    db_url: str | None = None,
) -> str:
    """Best official photo for a product name (website > overrides > DB > category)."""
    wp = _load_wp()
    fb = load_facebook_images()

    url = match_wp_image(product_name, wp)
    if not url:
        url = keyword_wp_match(product_name, wp)
    if not url:
        url = best_fuzzy_wp_match(product_name, wp)
    if not url:
        url = match_fb_image(product_name, fb)
    if not url and product_name in PRODUCT_IMAGE_OVERRIDES:
        url = PRODUCT_IMAGE_OVERRIDES[product_name]
    if not url:
        url = resolve_product_image_url(product_name, cat_name, sub_name)

    if db_url and not _is_generic_url(db_url):
        if _is_generic_url(url):
            return db_url
        return url

    return url or db_url or DEFAULT_PRODUCT_IMAGE


def _infer_letter_from_text(*parts: str) -> str:
    text = " ".join(p for p in parts if p).lower()
    if any(
        w in text
        for w in ("rudraksha", "spiritual", "gem", "shilajit", "yarsa", "coin", "mala")
    ):
        return "C"
    if any(
        w in text
        for w in ("nursery", "plant", "seedling", "sapling", "neem plant", "moringa plant")
    ):
        return "D"
    if any(
        w in text
        for w in (
            "gel",
            "soap",
            "cream",
            "cosmetic",
            "beauty",
            "henna",
            "indigo",
            "aloe",
            "rose water",
            "hair",
        )
    ):
        return "B"
    return "A"


def build_catalog_from_db(roots: list, store_links: dict[str, str]) -> list[dict]:
    """Flatten category tree into catalog items with resolved images."""
    items: list[dict] = []
    seen: set[str] = set()

    for cat in roots:
        cat_name = cat.get("name") or ""
        letter = _CAT_LETTERS.get(cat_name) or "A"
        for sub in cat.get("children") or []:
            sub_name = sub.get("name") or ""
            for p in sub.get("products") or []:
                name = (p.get("name") or "").strip()
                if not name:
                    continue
                key = name.lower()
                if key in seen:
                    continue
                seen.add(key)
                db_img = p.get("image_url")
                original = resolve_original_image(
                    name, cat_name, sub_name, db_img
                )
                items.append(
                    {
                        "name": name,
                        "cat": sub_name,
                        "cat_letter": letter,
                        "cat_root": cat_name,
                        "price": p.get("price") or 450,
                        "image_url": original,
                        "original_image": original,
                        "store_link": store_links.get(name)
                        or p.get("store_link")
                        or "https://saraworldwide.com.np/",
                        "source": "catalog",
                        "benefits": p.get("benefits"),
                        "effects": p.get("effects"),
                    }
                )

    return items, seen


def merge_gallery_into_catalog(
    items: list[dict], seen: set[str], store_links: dict[str, str]
) -> list[dict]:
    """Add gallery-only products (unique base titles) for collections & shop."""
    wp = _load_wp()
    by_base: dict[str, dict] = {}

    for entry in _load_all_website():
        base = gallery_base_title(entry["title"])
        if not base:
            continue
        key = base.lower()
        if key in seen:
            continue
        if key not in by_base:
            by_base[key] = entry
        elif "photo" in entry["title"].lower():
            continue
        else:
            by_base[key] = entry

    for base, entry in by_base.items():
        key = base.lower()
        if key in seen:
            continue
        seen.add(key)
        letter = _infer_letter_from_text(base, entry.get("title", ""))
        original = (
            entry["url"]
            or match_wp_image(base, wp)
            or resolve_original_image(base, "", "")
        )
        items.append(
            {
                "name": base,
                "cat": "From saraworldwide.com.np gallery",
                "cat_letter": letter,
                "cat_root": _letter_to_root(letter),
                "price": 450,
                "image_url": original,
                "original_image": original,
                "store_link": store_links.get(base)
                or entry.get("link")
                or "https://saraworldwide.com.np/",
                "source": "gallery",
                "benefits": None,
                "effects": None,
            }
        )

    return items


def _letter_to_root(letter: str) -> str:
    return {
        "A": "Category A: Food",
        "B": "Category B: Natural Cosmetics",
        "C": "Category C: Spirituals",
        "D": "Category D: Sara Nursery",
    }.get(letter, "Category A: Food")


def build_full_catalog(roots: list | None) -> dict:
    store_links = _load_store_links()
    items, seen = build_catalog_from_db(roots or [], store_links)
    items = merge_gallery_into_catalog(items, seen, store_links)

    by_letter: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0}
    for it in items:
        L = it.get("cat_letter") or "A"
        by_letter[L] = by_letter.get(L, 0) + 1

    image_map = {it["name"]: it["original_image"] for it in items}

    return {
        "products": items,
        "total": len(items),
        "by_category": by_letter,
        "image_map": image_map,
        "gallery_total": len(_load_all_website()),
    }
