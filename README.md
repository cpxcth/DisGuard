# DisGuard

DisGuard is a lightweight Discord moderation bot built with Python and discord.py. It focuses on fast, server-safe moderation actions exposed as slash commands and enforces permission and role-hierarchy checks before acting.

## Features

- `/ping` — confirm the bot is online and responding
- `/kick` — remove a server member
- `/ban` — ban a member from the server
- `/timeout` — temporarily mute a member for a duration from 1 minute up to 28 days
- `/untimeout` — remove an existing timeout
- `/clear` — delete recent messages from the current channel

## Architecture

- `bot.py` loads the moderation cog, syncs slash commands, and starts the bot
- `cogs/moderation.py` defines the slash-command handlers and permission error handling
- `services/moderation.py` contains the validation logic for moderation targets

## Requirements

- Python 3.10+
- Discord application token
- A Discord server where you have permission to add the bot

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your Discord bot token:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

## Running the bot

Start the bot with:

```bash
python bot.py
```

## License

This project free to use, fork and distribute. See the license file for details.
