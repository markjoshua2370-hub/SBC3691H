import logging
import os
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import pandascore_api as ps

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def _resolve_game(arg: str | None) -> str | None:
    if not arg:
        return None
    return ps.GAMES.get(arg.lower())


def _format_match(m: dict) -> str:
    opponents = m.get("opponents", [])
    names = [o["opponent"]["name"] for o in opponents if o.get("opponent")]
    matchup = " vs ".join(names) if names else "TBD"
    league = m.get("league", {}).get("name", "")
    begin_at = m.get("begin_at")
    when = ""
    if begin_at:
        try:
            when = datetime.fromisoformat(begin_at.replace("Z", "+00:00")).strftime("%b %d, %H:%M UTC")
        except ValueError:
            when = begin_at
    return f"#{m['id']} {matchup} - {league} - {when}"


def _format_result(m: dict) -> str:
    opponents = m.get("opponents", [])
    names = [o["opponent"]["name"] for o in opponents if o.get("opponent")]
    matchup = " vs ".join(names) if names else "Unknown"
    winner = m.get("winner", {})
    winner_name = winner.get("name") if winner else "No winner recorded"
    league = m.get("league", {}).get("name", "")
    return f"#{m['id']} {matchup} - {league}\nWinner: {winner_name}"


WELCOME_GAMES = [("League of Legends", "lol"), ("CS2", "cs2"), ("Dota 2", "dota2"), ("Valorant", "valorant")]


def _welcome_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(f"Upcoming {label}", callback_data=f"upcoming:{slug}")]
        for label, slug in WELCOME_GAMES
    ]
    return InlineKeyboardMarkup(buttons)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name or "there"
    await update.message.reply_text(
        f"Hey {name}! Welcome — I track esports schedules and results for you.\n\n"
        "Pick a game below to see what's coming up, or use these anytime:\n"
        "/upcoming <game> - upcoming matches (e.g. /upcoming lol)\n"
        "/results <game> - recent results\n"
        "/match <id> - details for a specific match\n"
        "/games - list supported game shortcuts",
        reply_markup=_welcome_keyboard(),
    )


async def _send_upcoming(send, game_slug: str) -> None:
    try:
        matches = ps.get_upcoming_matches(game_slug)
    except Exception:
        logger.exception("Upcoming matches request failed")
        await send("Couldn't reach the esports API. Try again shortly.")
        return

    if not matches:
        await send("No upcoming matches found for that game right now.")
        return

    lines = [_format_match(m) for m in matches]
    await send("Upcoming matches:\n" + "\n".join(lines) + "\n\nUse /match <id> for details.")


async def welcome_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    _, game_slug = query.data.split(":", 1)
    await _send_upcoming(query.message.reply_text, game_slug)


async def games_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = [f"{key} -> {slug}" for key, slug in ps.GAMES.items()]
    await update.message.reply_text("Supported games:\n" + "\n".join(lines))


async def upcoming(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    game_slug = _resolve_game(context.args[0] if context.args else None)
    if not game_slug:
        await update.message.reply_text("Usage: /upcoming <game>\nTry /games for the list of shortcuts.")
        return

    await _send_upcoming(update.message.reply_text, game_slug)


async def results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    game_slug = _resolve_game(context.args[0] if context.args else None)
    if not game_slug:
        await update.message.reply_text("Usage: /results <game>\nTry /games for the list of shortcuts.")
        return

    try:
        matches = ps.get_past_matches(game_slug)
    except Exception:
        logger.exception("Past matches request failed")
        await update.message.reply_text("Couldn't reach the esports API. Try again shortly.")
        return

    if not matches:
        await update.message.reply_text("No recent results found for that game.")
        return

    lines = [_format_result(m) for m in matches]
    await update.message.reply_text("Recent results:\n\n" + "\n\n".join(lines))


async def match_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /match <id>\nGet an id from /upcoming or /results")
        return

    try:
        match_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Match id must be a number.")
        return

    try:
        m = ps.get_match(match_id)
    except Exception:
        logger.exception("Match detail request failed")
        await update.message.reply_text("Couldn't reach the esports API, or that match id doesn't exist.")
        return

    opponents = m.get("opponents", [])
    names = [o["opponent"]["name"] for o in opponents if o.get("opponent")]
    matchup = " vs ".join(names) if names else "TBD"
    league = m.get("league", {}).get("name", "")
    serie = m.get("serie", {}).get("full_name", "")
    status = m.get("status", "unknown")
    number_of_games = m.get("number_of_games", "n/a")

    lines = [
        matchup,
        f"League: {league}",
        f"Series: {serie}",
        f"Status: {status}",
        f"Best of: {number_of_games}",
    ]

    winner = m.get("winner")
    if winner:
        lines.append(f"Winner: {winner.get('name')}")

    await update.message.reply_text("\n".join(lines))


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(welcome_button, pattern=r"^upcoming:"))
    app.add_handler(CommandHandler("games", games_list))
    app.add_handler(CommandHandler("upcoming", upcoming))
    app.add_handler(CommandHandler("results", results))
    app.add_handler(CommandHandler("match", match_detail))

    logger.info("Bot starting (polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
