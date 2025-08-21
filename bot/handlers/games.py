from telegram import Update
from telegram.ext import ContextTypes

GAMES = [
    ("/dice", "🎲 Dice"),
    ("/bowl", "🎳 Bowling"),
    ("/darts", "🎯 Darts"),
    ("/ball", "⚽ Football"),
    ("/bask", "🏀 Basketball"),
    ("/slots", "🎰 Slot Machine")
]

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    msg = "Available games:\n" + "\n".join([f"{emoji} — {cmd}" for cmd, emoji in GAMES])
    await update.message.reply_text(msg)
