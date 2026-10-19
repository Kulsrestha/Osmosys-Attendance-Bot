# Oqsha Telegram Attendance Bot

This bot provides `/checkin` and `/checkout` commands and sends multipart attendance requests.

## Safety

- `DRY_RUN=true` by default; no attendance API request is sent.
- Live commands can create real attendance records. Keep dry-run enabled until you intentionally decide to send a real request.
- Requests require HTTPS and the exact API host `osmosys-api.oqsha.com`.
- Never put API or Telegram tokens in source code or commit `.env`.

## Run locally

1. Install Python 3.11+.
2. Create a Telegram bot through BotFather.
3. Create `.env` locally with `BOT_TOKEN` and `ALLOWED_TELEGRAM_USER_IDS` (your numeric Telegram user ID). Add the API settings only when needed.
4. Install dependencies with `pip install -r requirements.txt`.
5. Run `python bot.py`.
6. Send `/start`, `/checkin`, or `/checkout` to your bot.

## Deployment

Configure the same values as environment variables in your hosting dashboard. Use `python bot.py` as the start command and install dependencies from `requirements.txt`. Include the `photos/` folder in the repository. Each check-in or check-out request randomly selects one supported image (`.jpg`, `.jpeg`, or `.png`) from that folder. Set `TEST_PHOTO_PATH` only if you want to force a specific image.

To enable API submission, configure `API_BASE_URL`, `API_TOKEN`, `ORGANISATION_ID`, `SITE_ID`, `USER_ID`, coordinates, and `TEST_PHOTO_PATH`. Set `DRY_RUN=false` only when you intend the command to create an attendance record. The bot returns the API status and response.
