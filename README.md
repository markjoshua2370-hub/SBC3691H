# Esports schedule & results Telegram bot

Fetches upcoming matches, recent results, and match details from PandaScore
for League of Legends, CS2, Dota 2, and Valorant.

## Commands
- `/upcoming <game>` - upcoming matches, e.g. `/upcoming lol`
- `/results <game>` - recent results
- `/match <id>` - full details for one match
- `/games` - list supported game shortcuts (lol, cs2, dota2, valorant)

## 1. Get your credentials

**Telegram bot token** - `@BotFather` on Telegram, `/newbot`

**PandaScore token**
1. Sign up at https://app.pandascore.co/signup (free, no credit card)
2. In your dashboard, find your API token under account settings
3. The free plan gives schedules, results, and pre-match data at 1,000
   requests/hour - live in-progress scores need a paid plan, which this bot
   doesn't use

## 2. Push to GitHub
New, separate repo. Files at the root: `bot.py`, `pandascore_api.py`,
`requirements.txt`, `Procfile`, `.gitignore`.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 3. Deploy on Railway
1. railway.app → **New Project** → **Deploy from GitHub repo**
2. **Variables** tab, add:
   - `TELEGRAM_BOT_TOKEN`
   - `PANDASCORE_TOKEN`
3. Confirm start command is `python bot.py`
4. Deploy, check logs for `Bot starting (polling)...`

## Extending it
- Add more games by adding entries to the `GAMES` dict in `pandascore_api.py`
  (PandaScore's docs list all supported game slugs).
- To notify a channel automatically when a followed team's match starts, add a
  scheduled job (`JobQueue`) that checks `/upcoming` on a timer.
