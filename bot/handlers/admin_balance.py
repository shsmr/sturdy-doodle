from telegram import Update
from telegram.ext import ContextTypes
import os
from bot.db.supabase import supabase

ADMIN_TELEGRAM_ID = os.getenv("ADMIN_TELEGRAM_ID")

async def setbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return
    args = context.args if context.args is not None else []
    if len(args) != 2:
        await update.message.reply_text("Usage: /setbalance <user_id> <amount>")
        return
    user_id, amount = args
    try:
        amount = float(amount)
        supabase.table("users").update({"balance": amount}).eq("id", int(user_id)).execute()
        await update.message.reply_text(f"✅ Set user {user_id} balance to ${amount:.2f}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def getbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return
    args = context.args if context.args is not None else []
    if len(args) != 1:
        await update.message.reply_text("Usage: /getbalance <user_id>")
        return
    user_id = args[0]
    try:
        resp = supabase.table("users").select("balance").eq("id", int(user_id)).execute()
        if resp.data:
            bal = resp.data[0]["balance"]
            await update.message.reply_text(f"User {user_id} balance: ${bal:.2f}")
        else:
            await update.message.reply_text("User not found.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def addbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return
    args = context.args if context.args is not None else []
    if len(args) != 2:
        await update.message.reply_text("Usage: /addbalance <user_id> <amount>")
        return
    user_id, amount = args
    try:
        amount = float(amount)
        resp = supabase.table("users").select("balance").eq("id", int(user_id)).execute()
        if resp.data:
            bal = resp.data[0]["balance"]
            new_bal = bal + amount
            supabase.table("users").update({"balance": new_bal}).eq("id", int(user_id)).execute()
            await update.message.reply_text(f"✅ Added ${amount:.2f} to user {user_id}. New balance: ${new_bal:.2f}")
        else:
            await update.message.reply_text("User not found.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def subbalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return
    args = context.args if context.args is not None else []
    if len(args) != 2:
        await update.message.reply_text("Usage: /subbalance <user_id> <amount>")
        return
    user_id, amount = args
    try:
        amount = float(amount)
        resp = supabase.table("users").select("balance").eq("id", int(user_id)).execute()
        if resp.data:
            bal = resp.data[0]["balance"]
            new_bal = bal - amount
            supabase.table("users").update({"balance": new_bal}).eq("id", int(user_id)).execute()
            await update.message.reply_text(f"✅ Subtracted ${amount:.2f} from user {user_id}. New balance: ${new_bal:.2f}")
        else:
            await update.message.reply_text("User not found.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def mybalance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return
    try:
        admin_id = ADMIN_TELEGRAM_ID if ADMIN_TELEGRAM_ID is not None else "0"
        resp = supabase.table("users").select("balance").eq("telegram_id", int(admin_id)).execute()
        if resp.data:
            bal = resp.data[0]["balance"]
            await update.message.reply_text(f"Your (admin) balance: ${bal:.2f}")
        else:
            await update.message.reply_text("Admin user not found in DB.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
