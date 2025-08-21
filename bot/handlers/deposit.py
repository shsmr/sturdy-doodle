from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.payments.oxapay import create_invoice

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    user_id = update.effective_user.id
    # Parse amount from command, default to 1 if not provided
    amount = 1.0
    if context.args:
        try:
            amount = float(context.args[0])
            if amount <= 0:
                raise ValueError
        except Exception:
            await update.message.reply_text("❌ Invalid amount. Usage: /deposit 10")
            return
    invoice_link = await create_invoice(user_id, amount=amount)
    if invoice_link and invoice_link.startswith("http"):
        keyboard = [[InlineKeyboardButton(f"💳 Pay ${amount:.2f} with OxaPay", url=invoice_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = (
            f"<b>Deposit</b>\n\n"
            f"Click the button below to deposit <b>${amount:.2f}</b> via OxaPay. "
            "After payment, your balance will be updated automatically."
        )
        await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup)
    else:
        await update.message.reply_text("⚠️ Deposit link unavailable. Please try again later.")
