# Madden 26 Discord Bot

Python Discord bot scaffold for connecting a Madden 26 franchise bot to EA auth data and Railway deployment.

## What It Does

- Creates a Discord slash-command bot.
- Generates the Madden 26 EA login URL.
- Exchanges an EA login `code` for account tokens.
- Stores EA tokens per Discord user.
- Supports console selection for PS5, Xbox Series X, PC, PS4, Xbox One, and Stadia.
- Provides the Madden 26 constants, entitlement mappings, Blaze service names, and week export options from your TypeScript data.
- Includes a clean EA client layer where franchise endpoints can be wired in.

## Commands

| Command | Purpose |
| --- | --- |
| `/ea_login` | Sends your Madden 26 EA login URL privately. |
| `/ea_connect code console` | Saves your EA account token after login. |
| `/ea_status` | Checks whether your EA token is saved. |
| `/ea_token_info` | Verifies the current EA token with EA token info. |
| `/ea_logout` | Deletes your saved EA token. |
| `/madden_constants` | Shows Madden 26 service/entitlement values for a console. |

## Railway Setup

1. Create a new Railway project.
2. Upload or connect this folder as your project.
3. Add these Railway variables:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_APPLICATION_ID=your_discord_application_id
EA_CLIENT_SECRET=your_ea_client_secret
TOKEN_ENCRYPTION_KEY=your_generated_fernet_key
```

Optional variables:

```env
EA_CLIENT_ID=MCA_26_COMP_APP
EA_AUTH_SOURCE=317239
EA_REDIRECT_URL=http://127.0.0.1/success
EA_MACHINE_KEY=444d362e8e067fe2
DATABASE_PATH=/data/madden26_bot.sqlite3
```

Generate `TOKEN_ENCRYPTION_KEY` with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.bot
```

## Important Notes

- Do not commit your real EA client secret or Discord bot token.
- Railway should run this as a worker, not a web server.
- The EA login redirect URL is `http://127.0.0.1/success`, so after logging in you copy the `code` from the browser URL and paste it into `/ea_connect`.
- Franchise/Blaze calls can be added in `src/ea_client.py` after token auth is confirmed.

