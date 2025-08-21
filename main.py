from bot.handlers.dice import dice
    app.add_handler(CommandHandler("dice", dice))
import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Handlers
from bot.handlers.start import start
from bot.handlers.balance import balance
from bot.handlers.help import help_command
from bot.handlers.games import games
from bot.handlers.bet import bet
from bot.handlers.referral import referral

from bot.handlers.dicegame import dicegame

# Load environment variables
load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

BOT_TOKEN = get_env("BOT_TOKEN")
SUPABASE_URL = get_env("SUPABASE_URL")
SUPABASE_KEY = get_env("SUPABASE_KEY")
OXAPAY_API_KEY = get_env("OXAPAY_API_KEY")
OXAPAY_WEBHOOK_SECRET = os.getenv("OXAPAY_WEBHOOK_SECRET")  # Optional
ADMIN_TELEGRAM_ID = get_env("ADMIN_TELEGRAM_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vegasrushbot")

async def main():
    # TODO: Connect to Supabase and OxaPay, log success
    logger.info("Starting VegasRushBot...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("games", games))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("dicegame", dicegame))

    logger.info("Bot started. Ready to accept commands.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
