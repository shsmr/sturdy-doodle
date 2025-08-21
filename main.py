

import asyncio
import logging
from bot.config import (
    BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY, OXAPAY_API_KEY, OXAPAY_WEBHOOK_SECRET, ADMIN_TELEGRAM_ID
)
from telegram.ext import Application, CommandHandler

# Handlers
from bot.handlers.start import start
from bot.handlers import balance
from bot.handlers.help import help_command
from bot.handlers.games import games
from bot.handlers.bet import bet
from bot.handlers.referral import referral
from bot.handlers.withdraw import withdraw
from bot.handlers.dicegame import dicegame
from bot.handlers import dice
from bot.handlers.deposit import deposit
from bot.handlers.admin_only import admin_only
from bot.handlers import admin_balance


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vegasrushbot")

async def main():
    # TODO: Connect to Supabase and OxaPay, log success
    logger.info("Starting VegasRushBot...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance.balance))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(balance.deposit_callback, pattern="^deposit$"))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("games", games))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CommandHandler("referral", referral))

    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("dicegame", dicegame))
    app.add_handler(CommandHandler("dice", dice.dice))
    # Handle user dice emoji replies
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.Dice.ALL, dice.dice_reply))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("admin_only", admin_only))
    # Admin-only balance management commands
    app.add_handler(CommandHandler("setbalance", admin_balance.setbalance))
    app.add_handler(CommandHandler("getbalance", admin_balance.getbalance))
    app.add_handler(CommandHandler("addbalance", admin_balance.addbalance))
    app.add_handler(CommandHandler("subbalance", admin_balance.subbalance))
    app.add_handler(CommandHandler("mybalance", admin_balance.mybalance))

    logger.info("Bot started. Ready to accept commands.")
    app.run_polling()

if __name__ == "__main__":
    import sys
    try:
        if sys.platform.startswith("win") or sys.platform == "darwin":
            asyncio.run(main())
        else:
            import nest_asyncio
            nest_asyncio.apply()
            asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        # fallback for environments where event loop is already running
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
