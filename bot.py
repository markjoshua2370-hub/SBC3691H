import logging
import os
import re

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def analyze(text: str) -> str:
    stripped = text.strip()
    words = len(re.findall(r"\b\w+\b", stripped)) if stripped else 0
    characters = len(text)
    characters_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    sentences = len([s for s in re.split(r"[.!?]+", stripped) if s.strip()])
    read_seconds = round((words / 200) * 60)
    read_time = f"{read_seconds}s" if read_seconds < 60 else f"{round(read_seconds / 60)}m"

    return (
        f"Words: {words}\n"
        f"Characters: {characters} ({characters_no_spaces} without spaces)\n"
        f"Sentences: {sentences}\n"
        f"Estimated read time: {read_time}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Word counter bot.\n\n"
        "Send me any text and I'll count words, characters, and sentences.\n"
        "Or use /count <text> directly."
    )


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /count <text>\nOr just send me a plain message.")
        return
    await update.message.reply_text(analyze(text))


async def count_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(analyze(update.message.text))


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("count", count_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_message))

    logger.info("Bot starting (polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
