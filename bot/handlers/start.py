from telegram import Update
from telegram.ext import ContextTypes
from bot.db.supabase import get_user, supabase
import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    username = update.effective_user.username or ""
    # Check if user exists
    user_resp = get_user(tg_id)
    if user_resp.data and len(user_resp.data) > 0:
        await update.message.reply_text(
            "🎰 Welcome back to VegasRushBot! Use /balance to check your balance or /help for instructions."
        )
        return
    # Register new user
    now = datetime.datetime.utcnow().isoformat()
    supabase.table("users").insert({
        "telegram_id": tg_id,
        "username": username,
        "created_at": now
    }).execute()
    await update.message.reply_text(
        "🎰 Welcome to VegasRushBot! Your account is created. Use /balance to check your balance or /help for instructions."
    )
