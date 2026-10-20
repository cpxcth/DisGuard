# DisGuard

DisGuard is a small Discord moderation bot written in Python with `discord.py`. It provides server-only slash commands for common moderation tasks and can serve multiple servers from one running bot instance.

## Commands

| Command | What it does | Required permission |
| --- | --- | --- |
| `/ping` | Check that the bot is responding | None |
| `/kick` | Remove a member from the server | Kick Members |
| `/ban` | Ban a member without deleting message history | Ban Members |
| `/timeout` | Timeout a member for 1 minute to 28 days | Moderate Members |
| `/untimeout` | Remove a member's timeout | Moderate Members |
| `/clear` | Delete 1 to 100 recent messages in a text channel | Manage Messages |

Moderation commands check permissions at runtime and prevent acting on yourself, the server owner, or members at or above the moderator's or bot's role. Responses are private to the command user.

## Requirements

- Python 3.10 or newer
- A Discord application and bot token

The bot uses slash commands and does not require the privileged Message Content intent.

## Run locally

```bash
git clone <repository-url>
cd DisGuard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

 Replace `<repository-url>` with the URL of your published repository. On Windows, activate the environment with `.venv\Scripts\activate`.

Copy `.env.example` to `.env` and replace the example value with your bot token:

```env
DISCORD_TOKEN=your_bot_token
```

Start the bot:

```bash
python bot.py
```

The bot syncs global slash commands at startup. Invite it with the `bot` and `applications.commands` scopes and grant only the permissions it needs: View Channels, Send Messages, Read Message History, Kick Members, Ban Members, Moderate Members, and Manage Messages. Place the bot's role above the members it should moderate. Invite the same bot application to each server; no server IDs need to be added to the code.

## Code layout

- `bot.py` is the entry point. It loads environment variables, creates the Discord bot, loads extensions, syncs slash commands, and starts the connection.
- `cogs/moderation.py` contains the moderation slash-command handlers and their user-facing responses. A Cog groups related commands together.
- `services/moderation.py` contains reusable moderation rules, such as checking that a target can be acted on. It does not register commands or start the bot.
- `requirements.txt` lists the Python dependencies.

This split keeps Discord startup separate from command behavior and reusable rules. To add a command, put its handler in the relevant Cog; move shared decisions or operations into `services/` when more than one handler needs them. `bot.py` loads the Cog by its Python module path, so no server IDs or per-server command registrations are needed.

## Project status

This is a learning starter. It does not include persistent moderation cases, per-server configuration, or a moderation log channel. Test it in a private server before using it in a community.

## License

DisGuard is released under [The Unlicense](LICENSE), dedicating it to the public domain where possible. You are free to use, fork, modify, and distribute it, including commercially, without an attribution requirement. The license includes a fallback permission grant for jurisdictions that do not recognize public-domain dedication.