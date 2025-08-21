import random
from telegram import Update
from telegram.ext import ContextTypes
from bot.db.supabase import get_user, supabase

HOUSE_EDGE = 0.02

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message:
        return
    tg_id = update.effective_user.id
    user_resp = get_user(tg_id)
    if not user_resp.data or len(user_resp.data) == 0:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    user = user_resp.data[0]
    balance = float(user.get("balance", 0))

    # Parse bet amount
    if not context.args:
        await update.message.reply_text(
            "🎲 <b>Play Dice</b>\n\n"
            "To play, type the command <code>/dice</code> with the desired bet.\n\n"
            "Examples:\n"
            "/dice 5.50 - to play for $5.50\n"
            "/dice half - to play for half of your balance\n"
            "/dice all - to play all-in",
            parse_mode="HTML"
        )
        return

    arg = context.args[0].lower()
    if arg == "all":
        bet_amount = balance
    elif arg == "half":
        bet_amount = balance / 2
    else:
        try:
            bet_amount = float(arg)
        except Exception:
            await update.message.reply_text("❌ Invalid bet amount. Usage: /dice 10 or /dice half or /dice all")
            return

    bet_amount = round(bet_amount, 2)
    if bet_amount <= 0 or bet_amount > balance:
        await update.message.reply_text(f"❌ Invalid bet. Your balance: ${balance:.2f}")
        return

    # Roll dice (1-6)
    player_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    # Determine win/loss
    if player_roll > bot_roll:
        payout = bet_amount * (1 - HOUSE_EDGE)
        new_balance = balance - bet_amount + payout
        result_msg = f"🎲 <b>Dice Game</b>\n\nYou: <b>{player_roll}</b>\nBot: <b>{bot_roll}</b>\n\n🏆 <b>You win!</b>\nPayout: <b>${payout:.2f}</b> (2% house edge)"
    elif player_roll < bot_roll:
        payout = 0
        new_balance = balance - bet_amount
        result_msg = f"🎲 <b>Dice Game</b>\n\nYou: <b>{player_roll}</b>\nBot: <b>{bot_roll}</b>\n\n😢 <b>You lose!</b>\nLost: <b>${bet_amount:.2f}</b>"
    else:
        payout = bet_amount
        new_balance = balance
        result_msg = f"🎲 <b>Dice Game</b>\n\nYou: <b>{player_roll}</b>\nBot: <b>{bot_roll}</b>\n\n🤝 <b>Draw!</b>\nYour bet is returned."

    # Update balance in DB
    supabase.table("users").update({"balance": new_balance}).eq("id", user["id"]).execute()
    # Store bet in DB
    supabase.table("bets").insert({
        "user_id": user["id"],
        "game_type": "dice",
        "bet_amount": bet_amount,
        "result": f"{player_roll}-{bot_roll}",
        "payout": payout
    }).execute()

    await update.message.reply_text(result_msg, parse_mode="HTML")
