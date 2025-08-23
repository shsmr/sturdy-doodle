from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None):
    msg_obj = message if message is not None else getattr(update, 'message', None)
    if not update.effective_user or not msg_obj:
        return
        help_text = """
    Available commands:
    /start - Register and get started
    /balance - Show your balance
    /deposit - Deposit crypto with OxaPay
    /bet - Place a bet
    /games - Show available games
    /referral - Get your referral link
    /withdraw - Request withdrawal
    /help - Show this help message
    """
        if return_text:
            return help_text
        if not update.effective_user or not msg_obj:
            return
        await msg_obj.reply_text(help_text)
