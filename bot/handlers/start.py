from telegram import Update
from telegram.ext import ContextTypes
from bot.db.supabase import get_user, supabase
import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    tg_id = update.effective_user.id
    username = update.effective_user.username or ""
    # Check if user exists
    user_resp = get_user(tg_id)
    keyboard = [
        [
            InlineKeyboardButton("💰 Check Balance", callback_data="show_balance"),
            InlineKeyboardButton("💳 Deposit", callback_data="deposit")
        ],
        [
            InlineKeyboardButton("🎲 Play Dice", callback_data="play_dice"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user_resp.data and len(user_resp.data) > 0:
        await update.message.reply_text(
            "🎰 <b>Welcome back to VegasRushBot!</b>\n\n"
            "<b>What would you like to do next?</b>",
            parse_mode="HTML",
            reply_markup=reply_markup
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
        "🎰 <b>Welcome to VegasRushBot!</b>\n\n"
        "Your account is created.\n\n<b>What would you like to do next?</b>",
        parse_mode="HTML",
        reply_markup=reply_markup
    )
