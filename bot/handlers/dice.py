from telegram import Update
from telegram.ext import ContextTypes

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🎲 <b>Play Dice</b>\n\n"
        "To play, type the command <code>/dice</code> with the desired bet.\n\n"
        "Examples:\n"
        "/dice 5.50 - to play for $5.50\n"
        "/dice half - to play for half of your balance\n"
        "/dice all - to play all-in"
    )
    await update.message.reply_text(msg, parse_mode="HTML")
