import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FRONTEND_URL

def send_reset_email(to_email: str, token: str):
    reset_link = f"{FRONTEND_URL}/reset-password.html?token={token}"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Sara Foods - Reset Your Password"
    msg["From"] = f"Sara Foods <{SMTP_USER}>"
    msg["To"] = to_email

    html = f"""
    <html><body style="font-family:sans-serif;background:#f8faf9;padding:40px;">
      <div style="max-width:500px;margin:0 auto;background:white;border-radius:16px;padding:40px;box-shadow:0 4px 20px rgba(0,0,0,0.08);">
        <img src="{FRONTEND_URL}/avatar.png" alt="Sara Foods" style="height:60px;border-radius:50%;margin-bottom:20px;">
        <h2 style="color:#1b5e20;">Reset Your Password</h2>
        <p style="color:#555;">You requested a password reset. Click the button below to set a new password.</p>
        <a href="{reset_link}" style="display:inline-block;background:linear-gradient(135deg,#1b5e20,#388e3c);color:white;text-decoration:none;padding:14px 32px;border-radius:50px;font-weight:700;margin:20px 0;">Reset Password</a>
        <p style="color:#888;font-size:0.85rem;">This link expires in 1 hour. If you did not request this, ignore this email.</p>
        <hr style="border:none;border-top:1px solid #eee;margin:20px 0;">
        <p style="color:#aaa;font-size:0.8rem;">Sara World Business Pvt. Ltd. | Kalanki-14, Kathmandu, Nepal</p>
      </div>
    </body></html>
    """
    msg.attach(MIMEText(html, "html"))

    # Try real SMTP, fall back to console print
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
    except Exception as e:
        # Dev fallback: print to console
        print(f"\n[EMAIL MOCK] Password reset link for {to_email}:\n{reset_link}\n")
