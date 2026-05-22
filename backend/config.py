import os
import logging
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SaraBackend")

def get_required_env(key: str, default: str = None) -> str:
    val = os.getenv(key, default)
    if not val or "YOUR_" in str(val) or "change-in-production" in str(val):
        if default is None:
            logger.error(f"CRITICAL: Missing required environment variable: {key}")
        else:
            logger.warning(f"Using insecure default for {key}. Please set this in your .env file.")
    return val

# ── Database ──────────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "sara_chatbot_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

# ── JWT ───────────────────────────────────────────────────────────────────────
JWT_SECRET     = get_required_env("JWT_SECRET", "sara-super-secret-key-change-in-production")
JWT_ALGORITHM  = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

# ── Google OAuth ──────────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID     = get_required_env("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_required_env("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI  = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")
GOOGLE_AUTH_URL      = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL     = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL  = "https://www.googleapis.com/oauth2/v3/userinfo"

# ── Gemini AI ─────────────────────────────────────────────────────────────────
GEMINI_API_KEY = get_required_env("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
AI_MODEL_NAME  = os.getenv("AI_MODEL_NAME", "gemini-1.5-flash")

# ── eSewa Payment ─────────────────────────────────────────────────────────────
ESEWA_PRODUCT_CODE = os.getenv("ESEWA_PRODUCT_CODE", "EPAYTEST")
ESEWA_SECRET_KEY   = os.getenv("ESEWA_SECRET_KEY", "8g8M8m8P8N8|8o8m8p8G8|8m8M8m8P8N8|8o8m8p8G8")
ESEWA_URL          = os.getenv("ESEWA_URL", "https://rc-epay.esewa.com.np/api/epay/main/v2/form")

# ── Email / SMTP ──────────────────────────────────────────────────────────────
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FRONTEND_URL  = os.getenv("FRONTEND_URL", "http://localhost:8000")
