from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db.database import get_db
from ..services.ai_service import get_ai_response

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

@router.get("/products")
def get_products():
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, parent_id FROM categories")
    cats = cur.fetchall()
    cur.execute("SELECT id, category_id, name, price, image_url FROM products")
    prods = cur.fetchall()
    conn.close()
    cat_map = {c["id"]: {**c, "children": [], "products": []} for c in cats}
    for p in prods:
        cid = p["category_id"]
        if cid in cat_map:
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
        "SELECT p.name, p.benefits, p.effects, p.price, p.image_url, c.name AS category "
        "FROM products p JOIN categories c ON p.category_id=c.id WHERE p.name LIKE %s LIMIT 1",
        (f"%{name}%",)
    )
    p = cur.fetchone()
    conn.close()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.post("/chat")
def chat(body: ChatBody):
    response = get_ai_response(body.message)
    return {"response": response}
