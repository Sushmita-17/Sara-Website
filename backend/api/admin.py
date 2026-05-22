from fastapi import APIRouter, Depends, HTTPException
from ..db.database import get_db
from ..services.auth_service import RoleChecker
from pydantic import BaseModel

router = APIRouter()
admin_only = RoleChecker(["admin"])
staff_or_admin = RoleChecker(["admin", "staff"])

class RoleUpdateBody(BaseModel):
    role: str

@router.get("/users")
def get_users(admin: dict = Depends(admin_only)):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, full_name, email, role, is_verified, created_at FROM users")
    users = cur.fetchall()
    conn.close()
    return users

@router.post("/users/{user_id}/role")
def update_user_role(user_id: int, body: RoleUpdateBody, admin: dict = Depends(admin_only)):
    if body.role not in ["customer", "staff", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET role=%s WHERE id=%s", (body.role, user_id))
    conn.commit()
    conn.close()
    return {"message": f"User role updated to {body.role}"}

@router.get("/stats")
def get_admin_stats(staff: dict = Depends(staff_or_admin)):
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM products")
    product_count = cur.fetchone()[0]
    
    cur.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    roles = dict(cur.fetchall())
    
    conn.close()
    return {
        "total_users": user_count,
        "total_products": product_count,
        "roles": roles
    }
