
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.db.supabase import get_user
from bot.payments.oxapay import create_static_address, create_invoice

async def deposit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or not query.from_user:
        return
    tg_id = query.from_user.id
    user_resp = get_user(tg_id)
    if not user_resp.data or len(user_resp.data) == 0:
        await query.answer("You are not registered.", show_alert=True)
        return
    user = user_resp.data[0]
    invoice_link = await create_invoice(user["id"], amount=0)
    if invoice_link and invoice_link.startswith("http"):
        await query.answer()
        await context.bot.send_message(
            chat_id=tg_id,
            text=f"💳 <b>Deposit</b>\nClick the link below to deposit via OxaPay:\n{invoice_link}",
            parse_mode="HTML"
        )
    else:
        await query.answer("Deposit link unavailable. Please try again later.", show_alert=True)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.db.supabase import get_user
from bot.payments.oxapay import create_static_address, create_invoice

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    tg_id = update.effective_user.id
    user_resp = get_user(tg_id)
    if not user_resp.data or len(user_resp.data) == 0:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    user = user_resp.data[0]
    bal = user.get("balance", 0)


    # Format balance in USD and crypto (for demo, just USDT)
    bal_usd = f"${bal:.2f}"
    bal_crypto = f"({bal:.5f} USDT)" if bal else ""


    # Inline buttons
    keyboard = []
    row = [
        InlineKeyboardButton("💳 Deposit", callback_data="deposit"),
        InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw")
    ]
    keyboard.append(row)
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
