from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Available commands:
/start - Register and get started
/balance - Show your balance
/bet - Place a bet
/games - Show available games
/referral - Get your referral link
/withdraw - Request withdrawal
/help - Show this help message
""")
