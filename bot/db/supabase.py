
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client


def get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

SUPABASE_URL = get_env("SUPABASE_URL")
SUPABASE_KEY = get_env("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Example function: get user by telegram_id
def get_user(telegram_id: int):
    return supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
