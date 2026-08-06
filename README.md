# Word counter Telegram bot

Send it any message and it replies with word count, character count, sentence
count, and estimated read time. Everything lives in one file, `bot.py`.

## 1. Get a bot token
1. Telegram â†’ message `@BotFather`
2. Send `/newbot`, follow the prompts
3. Copy the token

## 2. Push to GitHub
Create a **new, separate repo** for this bot (don't mix it into another bot's repo).
Files needed at the root: `bot.py`, `requirements.txt`, `Procfile`, `.gitignore`.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## 3. Deploy on Railway
1. railway.app â†’ **New Project** â†’ **Deploy from GitHub repo** â†’ select this repo
2. Go to **Variables** tab, add:
   - `TELEGRAM_BOT_TOKEN` = the token from BotFather
3. Check **Settings** â†’ deploy start command should be `python bot.py` (Railway
   should pick this up automatically from the `Procfile`)
4. Deploy, then check **Deploy logs** for `Bot starting (polling)...`

## Test it
Message your bot on Telegram: send `/start`, then just type any sentence, or try
`/count this is a test sentence`.
