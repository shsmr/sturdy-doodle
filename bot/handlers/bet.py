from telegram import Update
from telegram.ext import ContextTypes

async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    # TODO: Parse bet, deduct balance, roll dice, calculate win/loss, store bet
    await update.message.reply_text("Betting is coming soon!")
