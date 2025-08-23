import asyncio
import logging
from bot.config import (
    BOT_TOKEN, SUPABASE_URL, SUPABASE_KEY, OXAPAY_API_KEY, OXAPAY_WEBHOOK_SECRET, ADMIN_TELEGRAM_ID
)
from telegram.ext import Application, CommandHandler

# Handlers
from bot.handlers.start import start
from bot.handlers.balance import balance, deposit_callback
from bot.handlers.help import help_command
from bot.handlers.games import games
from bot.handlers.bet import bet
from bot.handlers.referral import referral
from bot.handlers.withdraw import withdraw
from bot.handlers.dicegame import dicegame
from bot.handlers.dice import dice, dice_reply
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
    app.add_handler(CommandHandler("balance", balance))
    from telegram.ext import CallbackQueryHandler
    app.add_handler(CallbackQueryHandler(deposit_callback, pattern="^deposit$"))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("games", games))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CommandHandler("referral", referral))

    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("dicegame", dicegame))
    app.add_handler(CommandHandler("dice", dice))
    # Handle user dice emoji replies
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.Dice.ALL, dice_reply))
    app.add_handler(CommandHandler("deposit", deposit))
    app.add_handler(CommandHandler("admin_only", admin_only))
    # Admin-only balance management commands
    app.add_handler(CommandHandler("setbalance", admin_balance.setbalance))
    app.add_handler(CommandHandler("getbalance", admin_balance.getbalance))
    app.add_handler(CommandHandler("addbalance", admin_balance.addbalance))
    app.add_handler(CommandHandler("subbalance", admin_balance.subbalance))
    app.add_handler(CommandHandler("mybalance", admin_balance.mybalance))

    # Navigation callback handler
    async def nav_callback(update, context):
        query = update.callback_query
        if not query:
            return
        data = query.data
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        # Go Back button always present
        go_back_btn = [InlineKeyboardButton("⬅️ Go Back", callback_data="go_back")]
        if data == "show_balance":
            await query.edit_message_text(
                text=await balance(update, context, message=None, return_text=True),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("💳 Deposit", callback_data="deposit"), InlineKeyboardButton("🏧 Withdraw", callback_data="withdraw")],
                    [InlineKeyboardButton("🎲 Play Dice", callback_data="play_dice")],
                    go_back_btn
                ])
            )
            await query.answer()
        elif data == "play_dice":
            await query.edit_message_text(
                text=await dice(update, context, message=None, args=None, return_text=True),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    go_back_btn
                ])
            )
            await query.answer()
        elif data == "deposit":
            await query.edit_message_text(
                text="<b>Deposit</b>\n\nTo deposit, click the button below to generate a deposit link.\n\n<b>Instructions:</b>\n1. Click 'Generate Deposit Link'\n2. Enter the amount you want to deposit (USD only, e.g. 10)\n3. You will receive a payment button.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Generate Deposit Link", callback_data="generate_deposit_link")],
                    go_back_btn
                ])
            )
            await query.answer()
        elif data == "generate_deposit_link":
            await query.edit_message_text(
                text="<b>Enter the deposit amount (USD only):</b>\nJust send the number, e.g. 10",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([go_back_btn])
            )
            # Set state for next message
            context.user_data['awaiting_deposit_amount'] = True
            await query.answer()
        elif data == "go_back":
            # Go back to main menu
            from bot.handlers.start import start
            await start(update, context, edit_message=query)
            await query.answer()
        elif data == "help":
            await query.edit_message_text(
                text=await help_command(update, context, message=None, return_text=True),
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([go_back_btn])
            )
            await query.answer()
        else:
            await query.answer()

    app.add_handler(CallbackQueryHandler(nav_callback, pattern="^(show_balance|play_dice|deposit|help|generate_deposit_link|go_back)$"))

    # Handle deposit amount input after 'Generate Deposit Link'
    async def deposit_amount_handler(update, context):
        if context.user_data.get('awaiting_deposit_amount'):
            try:
                amount = float(update.message.text.strip())
                if amount <= 0:
                    raise ValueError
            except Exception:
                await update.message.reply_text("❌ Invalid amount. Please enter a positive number (USD only).", reply_markup=None)
                return
            from bot.payments.oxapay import create_invoice
            user_id = update.effective_user.id
            invoice_link = await create_invoice(user_id, amount=amount)
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [[InlineKeyboardButton(f"💳 Pay ${amount:.2f} with OxaPay", url=invoice_link)], [InlineKeyboardButton("⬅️ Go Back", callback_data="go_back")]]
            await update.message.reply_text(
                f"<b>Deposit</b>\n\nClick the button below to deposit <b>${amount:.2f}</b> via OxaPay. After payment, your balance will be updated automatically.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            context.user_data['awaiting_deposit_amount'] = False
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), deposit_amount_handler))

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
