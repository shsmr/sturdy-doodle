from fastapi import FastAPI, Request, HTTPException
from bot.db.supabase import supabase
import logging
import os

app = FastAPI()

@app.post("/oxapay-webhook")
async def oxapay_webhook(request: Request):
    data = await request.json()
    logging.getLogger("vegasrushbot").info(f"OxaPay webhook received: {data}")

    # Basic validation (customize as needed)
    if "order_id" not in data or "amount" not in data or "status" not in data:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")
    if data["status"] != "paid":
        return {"ok": True, "msg": "Not a paid status, ignored."}

    # Extract user_id from order_id (format: uuid or USER-<id>)
    order_id = data["order_id"]
    user_id = None
    if order_id.startswith("USER-"):
        try:
            user_id = int(order_id.split("-")[1])
        except Exception:
            pass
    # If you use uuid order_ids, you may need to map them to users in your DB
    if not user_id:
        logging.getLogger("vegasrushbot").warning(f"Could not extract user_id from order_id: {order_id}")
        return {"ok": False, "msg": "User not found"}

    amount = float(data["amount"])
    # Update user balance atomically
    resp = supabase.table("users").update({"balance": supabase.table("users").select("balance").eq("id", user_id).execute().data[0]["balance"] + amount}).eq("id", user_id).execute()
    logging.getLogger("vegasrushbot").info(f"User {user_id} balance updated by {amount}")
    return {"ok": True}

# To run: uvicorn webhook_server:app --host 0.0.0.0 --port 8000
