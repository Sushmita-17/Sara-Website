import secrets, hashlib
from datetime import datetime, timedelta
from urllib.parse import quote
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from ..db.database import get_db
from ..services.auth_service import hash_password, verify_password, create_token, get_current_user
from ..services.email_service import send_reset_email
from ..config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_AUTH_URL, GOOGLE_TOKEN_URL, GOOGLE_USERINFO_URL, FRONTEND_URL
import httpx

router = APIRouter()

# ── Schemas ───────────────────────────────────────────────────────────────────
class RegisterBody(BaseModel):
    full_name: str
    email: str
    password: str

class LoginBody(BaseModel):
    email: str
    password: str

class ForgotBody(BaseModel):
    email: str

class ResetBody(BaseModel):
    token: str
    new_password: str


# ── Register ──────────────────────────────────────────────────────────────────
@router.post("/register")
def register(body: RegisterBody):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email=%s", (body.email,))
    if cur.fetchone():
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = hash_password(body.password)
    cur.execute("INSERT INTO users (full_name, email, password_hash) VALUES (%s,%s,%s)",
                (body.full_name, body.email, hashed))
    conn.commit()
    user_id = cur.lastrowid
    token = create_token({"sub": str(user_id), "email": body.email, "name": body.full_name, "role": "customer"})
    conn.close()
    return {"access_token": token, "token_type": "bearer", "name": body.full_name, "role": "customer"}


# ── Login ─────────────────────────────────────────────────────────────────────
@router.post("/login")
def login(body: LoginBody):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s", (body.email,))
    user = cur.fetchone()
    conn.close()
    if not user or not user["password_hash"] or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"sub": str(user["id"]), "email": user["email"], "name": user["full_name"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "name": user["full_name"], "role": user["role"]}


# ── Google OAuth ──────────────────────────────────────────────────────────────
@router.get("/google")
def google_login():
    params = (
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
    )
    return RedirectResponse(GOOGLE_AUTH_URL + params)

@router.get("/google/callback")
async def google_callback(code: str):
    async with httpx.AsyncClient() as client:
        # Exchange code for tokens
        token_resp = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        tokens = token_resp.json()
        if "error" in tokens:
            raise HTTPException(status_code=400, detail=tokens.get("error_description", "Google auth failed"))

        # Get user info
        info_resp = await client.get(GOOGLE_USERINFO_URL,
                                     headers={"Authorization": f"Bearer {tokens['access_token']}"})
        guser = info_resp.json()

    email = guser.get("email")
    name  = guser.get("name", "")
    gid   = guser.get("sub")

    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users (full_name, email, google_id, is_verified) VALUES (%s,%s,%s,1)",
                    (name, email, gid))
        conn.commit()
        user_id = cur.lastrowid
        role = "customer"
    else:
        user_id = user["id"]
        role = user["role"]
        if not user.get("google_id"):
            cur.execute("UPDATE users SET google_id=%s, is_verified=1 WHERE id=%s", (gid, user_id))
            conn.commit()

    conn.close()
    token = create_token({"sub": str(user_id), "email": email, "name": name, "role": role})
    # Dedicated callback page (same origin as app — avoids localhost:5500 iframe errors)
    safe_name = quote(name or "User")
    return RedirectResponse(
        f"{FRONTEND_URL}/auth-callback.html?token={token}&name={safe_name}&role={role}"
    )


# ── Me ────────────────────────────────────────────────────────────────────────
@router.get("/me")
def get_me(user: dict = __import__('fastapi').Depends(get_current_user)):
    return user


# ── Forgot Password ───────────────────────────────────────────────────────────
@router.post("/forgot-password")
def forgot_password(body: ForgotBody):
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM users WHERE email=%s", (body.email,))
    user = cur.fetchone()
    if not user:
        # Don't reveal if email exists
        conn.close()
        return {"message": "If that email exists, a reset link has been sent."}

    # Generate secure token
    raw_token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    expires = datetime.utcnow() + timedelta(hours=1)

    cur.execute("DELETE FROM password_reset_tokens WHERE user_id=%s", (user["id"],))
    cur.execute("INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s,%s,%s)",
                (user["id"], hashed_token, expires))
    conn.commit()
    conn.close()

    send_reset_email(body.email, raw_token)
    return {"message": "If that email exists, a reset link has been sent."}


# ── Reset Password ────────────────────────────────────────────────────────────
@router.post("/reset-password")
def reset_password(body: ResetBody):
    hashed_token = hashlib.sha256(body.token.encode()).hexdigest()
    conn = get_db()
    cur  = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM password_reset_tokens WHERE token=%s", (hashed_token,))
    record = cur.fetchone()

    if not record or record["expires_at"] < datetime.utcnow():
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    new_hash = hash_password(body.new_password)
    cur.execute("UPDATE users SET password_hash=%s WHERE id=%s", (new_hash, record["user_id"]))
    cur.execute("DELETE FROM password_reset_tokens WHERE token=%s", (hashed_token,))
    conn.commit()
    conn.close()
    return {"message": "Password reset successfully. You can now log in."}
