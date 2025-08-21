import os
import httpx

import json
import uuid
OXAPAY_API_KEY = os.getenv("OXAPAY_API_KEY")
OXAPAY_WEBHOOK_SECRET = os.getenv("OXAPAY_WEBHOOK_SECRET")

# Example: create deposit address (stub)
BASE_URL = "https://api.oxapay.com/v1/payment"
# Example: verify webhook signature (stub)

# Generate a static deposit address (one per user)
async def create_static_address(user_id: int):
    url = f"{BASE_URL}/static-address"
    data = {
        "network": "TRON",
        "to_currency": "USDT",
        "auto_withdrawal": False,
        "order_id": f"USER-{user_id}",
        "description": f"Deposit for user {user_id}"
    }
    headers = {
        "merchant_api_key": OXAPAY_API_KEY,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        result = resp.json()
        return result.get("result", {}).get("address", "Error: No address")

async def create_invoice(user_id: int, amount: float = 0):
    url = f"{BASE_URL}/invoice"
    order_id = str(uuid.uuid4())
    data = {
        "amount": amount if amount > 0 else 1,
        "currency": "USD",
        "lifetime": 30,
        "fee_paid_by_payer": 1,
        "under_paid_coverage": 2.5,
        "to_currency": "USDT",
        "auto_withdrawal": False,
        "mixed_payment": True,
        "return_url": "https://example.com/success",
        "order_id": order_id,
        "thanks_message": "Thanks for your deposit!",
        "description": f"Deposit for user {user_id}",
        "sandbox": False
    }
    headers = {
        "merchant_api_key": OXAPAY_API_KEY,
        "Content-Type": "application/json"
    }
    import logging
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=data, headers=headers)
        result = resp.json()
        logging.getLogger("vegasrushbot").info(f"OxaPay invoice response: {result}")
    # OxaPay returns payment_url in 'data' field
    return result.get("data", {}).get("payment_url", "Error: No link")
def verify_webhook_signature(headers, body):
    # TODO: Implement signature verification per OxaPay docs
    return True
