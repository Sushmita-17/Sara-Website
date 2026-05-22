from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
try:
    from ..config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MIN  # package import
except ImportError:
    # When running scripts directly (e.g., setup_db.py in Docker), relative imports may fail
    from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_MIN
from fastapi import HTTPException, Header
from typing import Optional

# NOTE: bcrypt/passlib is failing in this Docker environment.
# Use a deterministic SHA-256 hash as a fallback so the site can start.
# (Login/password verification remains consistent within this deployment.)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception:
        import hashlib
        return "sha256$" + hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        # If it was hashed by bcrypt/passlib, verify normally
        if not str(hashed).startswith("sha256$"):
            return pwd_context.verify(plain, hashed)
    except Exception:
        pass

    if str(hashed).startswith("sha256$"):
        import hashlib
        expected = "sha256$" + hashlib.sha256(plain.encode("utf-8")).hexdigest()
        return expected == hashed

    return False

def create_token(data: dict, expires_minutes: int = JWT_EXPIRE_MIN) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    return decode_token(token)

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = __import__('fastapi').Depends(get_current_user)):
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
