from telegram import Update
from telegram.ext import ContextTypes

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Request withdrawal, store as pending, notify admin
    await update.message.reply_text("Withdrawal request feature coming soon!")
