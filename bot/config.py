import os
from dotenv import load_dotenv

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
