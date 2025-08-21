from telegram import Update
from telegram.ext import ContextTypes

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Generate referral link and show earnings
    await update.message.reply_text("Your referral link: (demo)")
