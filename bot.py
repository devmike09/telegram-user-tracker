
import csv
import os
from datetime import datetime, timezone

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
CSV_FILE = os.environ.get("CSV_FILE", "users.csv")


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    if user is None:
        return

    file_exists = os.path.exists(CSV_FILE)
    already_saved = False

    if file_exists:
        with open(
            CSV_FILE, "r", newline="", encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)
            already_saved = any(
                row["user_id"] == str(user.id)
                for row in reader
            )

    if not already_saved:
        with open(
            CSV_FILE, "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)

            if not file_exists or os.path.getsize(CSV_FILE) == 0:
                writer.writerow([
                    "user_id",
                    "username",
                    "first_name",
                    "last_name",
                    "first_started_at_utc",
                ])

            writer.writerow([
                user.id,
                user.username or "",
                user.first_name or "",
                user.last_name or "",
                datetime.now(timezone.utc).isoformat(),
            ])

    await update.message.reply_text(
        f"Welcome, {user.first_name}! "
        "You have successfully started the bot."
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
