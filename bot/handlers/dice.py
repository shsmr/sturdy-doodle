
from telegram import Update, Message, Dice
from telegram.ext import ContextTypes
from bot.db.supabase import get_user, supabase

HOUSE_EDGE = 0.02

# In-memory store for pending dice games: {user_id: {"bet": float, "bot_value": int, "msg_id": int}}
pending_dice_games = {}

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None, args=None):
    msg_obj = message if message is not None else getattr(update, 'message', None)
    args_val = args if args is not None else getattr(context, 'args', None)
    if not update.effective_user or not msg_obj:
        return

    tg_id = update.effective_user.id
    # Always fetch latest balance from DB
    user_resp = get_user(tg_id)
        if not user_resp.data or len(user_resp.data) == 0:
            if return_text:
                return "You are not registered. Use /start first."
            await msg_obj.reply_text("You are not registered. Use /start first.")
            return
    user = user_resp.data[0]
    # Fetch balance again to avoid stale value
    balance = float(user.get("balance", 0))

    # Parse bet amount
    if not args_val:
            msg = (
                "🎲 <b>Play Dice (Emoji Game)</b>\n\n"
                "To play, type the command <code>/dice</code> with the desired bet.\n\n"
                "Examples:\n"
                "/dice 5.50 - to play for $5.50\n"
                "/dice half - to play for half of your balance\n"
                "/dice all - to play all-in\n\n"
                "How to play:\n"
                "1. Bot rolls the dice emoji.\n"
                "2. You reply with your own 🎲 emoji (use the dice button).\n"
                "3. Higher roll wins!"
            )
            if return_text:
                return msg
            await msg_obj.reply_text(msg, parse_mode="HTML")
            return

    arg = args_val[0].lower()

    if arg == "all":
        bet_amount = round(balance, 2)
    elif arg == "half":
        bet_amount = round(balance / 2, 2)
    else:
        try:
            bet_amount = round(float(arg), 2)
        except Exception:
            await msg_obj.reply_text("❌ Invalid bet amount. Usage: /dice 10 or /dice half or /dice all")
            return

    # Allow betting full balance, accounting for floating point error
    if bet_amount <= 0 or bet_amount > balance + 0.01:
        await msg_obj.reply_text(f"❌ Invalid bet. Your balance: ${balance:.2f}")
        return

    # Deduct bet immediately, clamp to zero to avoid negative balances
    new_balance = max(0, round(balance - bet_amount, 2))
    supabase.table("users").update({"balance": new_balance}).eq("telegram_id", tg_id).execute()

    # Bot sends dice emoji
    dice_msg: Message = await msg_obj.reply_dice(emoji="🎲")
    bot_value = dice_msg.dice.value if dice_msg.dice else None
    if not bot_value:
        await msg_obj.reply_text("❌ Failed to roll dice. Try again.")
        return

    # Store pending game
    pending_dice_games[tg_id] = {
        "bet": bet_amount,
        "bot_value": bot_value,
        "msg_id": dice_msg.message_id,
        "old_balance": balance
    }

    await msg_obj.reply_text(
        f"You bet: <b>${bet_amount:,.2f}</b>\n"
        f"Old balance: <b>${balance:,.2f}</b>\n"
        "Now reply with your own 🎲 dice emoji (use the dice button below).",
        parse_mode="HTML"
    )

# Handler for user dice replies
async def dice_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.message or not update.message.dice:
        return
    tg_id = update.effective_user.id
    if tg_id not in pending_dice_games:
        return  # No pending game
    game = pending_dice_games.pop(tg_id)
    user_value = update.message.dice.value
    bot_value = game["bot_value"]
    bet_amount = game["bet"]
    old_balance = game["old_balance"]

    # Get user and balance
    user_resp = get_user(tg_id)
    if not user_resp.data or len(user_resp.data) == 0:
        await update.message.reply_text("You are not registered. Use /start first.")
        return
    user = user_resp.data[0]
    balance = float(user.get("balance", 0))

    # Determine win/loss
    if user_value > bot_value:
        total_returned = bet_amount * 2 * (1 - HOUSE_EDGE)
        net_profit = total_returned - bet_amount
        new_balance = balance + total_returned
        payout = total_returned
        result_msg = (
            f"🎲 <b>Dice Game</b>\n\n"
            f"You: <b>{user_value}</b>\nBot: <b>{bot_value}</b>\n\n"
            f"🏆 <b>You win!</b>\n"
            f"Bet: <b>${bet_amount:,.2f}</b>\n"
            f"Total returned: <b>${total_returned:,.2f}</b>\n"
            f"Net profit (after 2% house edge): <b>${net_profit:,.2f}</b>\n"
            f"Old balance: <b>${old_balance:,.2f}</b>\nNew balance: <b>${new_balance:,.2f}</b>"
        )
    elif user_value == bot_value:
        payout = bet_amount
        new_balance = balance + bet_amount
        result_msg = (
            f"🎲 <b>Dice Game</b>\n\n"
            f"You: <b>{user_value}</b>\nBot: <b>{bot_value}</b>\n\n"
            f"🤝 <b>Draw!</b>\nYour bet is returned.\n"
            f"Old balance: <b>${old_balance:,.2f}</b>\nNew balance: <b>${old_balance:,.2f}</b>"
        )
    else:
        payout = 0
        new_balance = balance
        result_msg = (
            f"🎲 <b>Dice Game</b>\n\n"
            f"You: <b>{user_value}</b>\nBot: <b>{bot_value}</b>\n\n"
            f"❌ <b>You lose!</b>\n"
            f"Bet: <b>${bet_amount:,.2f}</b>\n"
            f"Old balance: <b>${old_balance:,.2f}</b>\nNew balance: <b>${new_balance:,.2f}</b>"
        )

    # Update balance in DB
    supabase.table("users").update({"balance": new_balance}).eq("telegram_id", tg_id).execute()
    # Store bet in DB
    supabase.table("bets").insert({
        "user_id": user["id"],
        "game_type": "dice",
        "bet_amount": bet_amount,
        "result": f"{user_value}-{bot_value}",
        "payout": payout
    }).execute()

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [
        [
            InlineKeyboardButton("🎲 Play Again", callback_data="play_dice"),
            InlineKeyboardButton("💰 Check Balance", callback_data="show_balance")
        ],
        [
            InlineKeyboardButton("💳 Deposit", callback_data="deposit")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(result_msg, parse_mode="HTML", reply_markup=reply_markup)
