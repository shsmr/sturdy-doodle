from telegram import Update
from telegram.ext import ContextTypes
import random

# This is a simple 1v1 dice game demo
# In production, you would store sessions in DB and handle concurrency

async def dicegame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    player_name = user.first_name or user.username or "Player"
    bot_name = "Bot"

    # Simulate dice rolls
    player_score = random.randint(1, 6)
    bot_score = random.randint(1, 6)

    await update.message.reply_text(f"🎲 <b>Dice Game!</b>\n\n{player_name}: {player_score}\n{bot_name}: {bot_score}", parse_mode="HTML")

    if player_score > bot_score:
        await update.message.reply_text(f"🏆 <b>Game over!</b>\n\nScore:\n{player_name} • {player_score}\n{bot_name} • {bot_score}\n\n{player_name} wins $2.00!", parse_mode="HTML")
    elif bot_score > player_score:
        await update.message.reply_text(f"🏆 <b>Game over!</b>\n\nScore:\n{player_name} • {player_score}\n{bot_name} • {bot_score}\n\n{bot_name} wins $2.00!", parse_mode="HTML")
    else:
        await update.message.reply_text(f"🤝 <b>It’s a draw!</b>\n\nScore:\n{player_name} • {player_score}\n{bot_name} • {bot_score}", parse_mode="HTML")
