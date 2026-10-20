###########################################################################################################
# Run `python bot.py` to start the bot. Make sure you have a .env file with your Discord bot token in it. #
# Grab a token from https://discord.com/developers/applications                                           #
#                                                                                                         #
# cogs/ includes the commands for the bot                                                                 #
# services/ includes the logic for the commands, which is imported into cogs/                             #
###########################################################################################################

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


class ModerationBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.moderation")
        await self.tree.sync()
        logging.info("Slash commands synced")


bot = ModerationBot()


def main() -> None:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN is missing. Add it to a .env file; see README.md.")
    bot.run(token)


if __name__ == "__main__":
    main()