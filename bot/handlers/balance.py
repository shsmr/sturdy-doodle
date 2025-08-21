
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.db.supabase import get_user
from bot.payments.oxapay import create_static_address, create_invoice

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    user_resp = get_user(tg_id)
    if not user_resp.data or len(user_resp.data) == 0:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    user = user_resp.data[0]
    bal = user.get("balance", 0)
    static_addr = await create_static_address(user["id"])
    invoice_link = await create_invoice(user["id"], amount=0)

    # Format balance in USD and crypto (for demo, just USDT)
    bal_usd = f"${bal:.2f}"
    bal_crypto = f"({bal:.5f} USDT)" if bal else ""

    # Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("💳 Deposit", url=invoice_link),
            InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Styled message
    msg = (
        f"<code>/balance</code>\n"
        f"Your balance: <b>{bal_usd}</b> {bal_crypto}"
    )
    await update.message.reply_text(
        msg,
        parse_mode="HTML",
        reply_markup=reply_markup
    )
