from telegram import Update
from telegram.ext import ContextTypes

from bot.config import ADMIN_TELEGRAM_ID

ADMIN_COMMANDS = [
    "/setbalance &lt;user_id&gt; &lt;amount&gt; — Set a user's balance",
    "/getbalance &lt;user_id&gt; — Get a user's balance",
    "/addbalance &lt;user_id&gt; &lt;amount&gt; — Add to a user's balance",
    "/subbalance &lt;user_id&gt; &lt;amount&gt; — Subtract from a user's balance",
    "/mybalance — Show the admin's own balance"
]

async def admin_only(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    if str(update.effective_user.id) != str(ADMIN_TELEGRAM_ID):
        return  # Silent for non-admins
    msg = "<b>Admin-only commands:</b>\n\n" + "\n".join(ADMIN_COMMANDS)
    await update.message.reply_text(msg, parse_mode="HTML")
