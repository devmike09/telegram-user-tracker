import os
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = int(os.environ["ADMIN_CHAT_ID"])


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user
    message = update.effective_message

    if user is None or message is None:
        return

    username = f"@{user.username}" if user.username else "Not set"
    first_name = user.first_name or "Not provided"
    user_id = user.id
    started_at = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    # Notify the admin, but don't stop the welcome message
    # if the admin notification fails.
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                "🔔 New user started your bot!\n\n"
                f"Username: {username}\n"
                f"First name: {first_name}\n"
                f"Telegram ID: {user_id}\n"
                f"Started at: {started_at}"
            ),
        )
    except Exception:
        print("Could not send admin notification.")

    await message.reply_text(
        f"Welcome, {first_name}!\n"
        "You've successfully started the bot."
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
