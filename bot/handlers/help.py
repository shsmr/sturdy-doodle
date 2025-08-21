from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    await update.message.reply_text("""
Available commands:
/start - Register and get started
/balance - Show your balance
/deposit - Deposit crypto with OxaPay
/bet - Place a bet
/games - Show available games
/referral - Get your referral link
/withdraw - Request withdrawal
/help - Show this help message
""")
