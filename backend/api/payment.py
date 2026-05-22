import hmac
import hashlib
import base64
import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List
from ..db.database import get_db
from ..services.auth_service import get_current_user
from ..config import ESEWA_PRODUCT_CODE, ESEWA_SECRET_KEY, ESEWA_URL, FRONTEND_URL

router = APIRouter(prefix="/payment", tags=["payment"])

class OrderInitiate(BaseModel):
    amount: float
    payment_method: str  # 'esewa' or 'qr'

def generate_esewa_signature(secret_key: str, data: str) -> str:
    hmac_key = secret_key.encode('utf-8')
    message = data.encode('utf-8')
    signature = hmac.new(hmac_key, message, hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

@router.post("/initiate")
async def initiate_payment(order: OrderInitiate, current_user: dict = Depends(get_current_user)):
    transaction_uuid = str(uuid.uuid4())
    
    # Save pending order to DB
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO orders (user_id, total_amount, status, payment_method, transaction_uuid) VALUES (%s, %s, %s, %s, %s)",
            (current_user["id"], order.amount, "pending", order.payment_method, transaction_uuid)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to create order")
    finally:
        conn.close()

    if order.payment_method == "esewa":
        # Signature fields: total_amount,transaction_uuid,product_code
        message = f"total_amount={order.amount},transaction_uuid={transaction_uuid},product_code={ESEWA_PRODUCT_CODE}"
        signature = generate_esewa_signature(ESEWA_SECRET_KEY, message)
        
        return {
            "method": "esewa",
            "url": ESEWA_URL,
            "fields": {
                "amount": str(order.amount),
                "tax_amount": "0",
                "total_amount": str(order.amount),
                "transaction_uuid": transaction_uuid,
                "product_code": ESEWA_PRODUCT_CODE,
                "product_service_charge": "0",
                "product_delivery_charge": "0",
                "success_url": f"{FRONTEND_URL}/success.html",
                "failure_url": f"{FRONTEND_URL}/failure.html",
                "signed_field_names": "total_amount,transaction_uuid,product_code",
                "signature": signature
            }
        }
    
    return {
        "method": "qr",
        "transaction_uuid": transaction_uuid,
        "message": "Please scan the QR code to pay"
    }

@router.get("/callback")
async def payment_callback(data: str):
    # eSewa returns base64 encoded JSON in 'data' param
    try:
        decoded_data = base64.b64decode(data).decode('utf-8')
        import json
        payment_info = json.loads(decoded_data)
        
        # Verify transaction with eSewa (optional but recommended)
        # For now, we update the status based on the callback data
        if payment_info.get("status") == "COMPLETE":
            tx_uuid = payment_info.get("transaction_uuid")
            conn = get_db()
            cur = conn.cursor()
            cur.execute("UPDATE orders SET status='completed' WHERE transaction_uuid=%s", (tx_uuid,))
            conn.commit()
            conn.close()
            return {"message": "Payment verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid payment data")

    return {"message": "Payment pending or failed"}
