import logging
from datetime import timedelta

import discord
from discord import app_commands
from discord.ext import commands

from services.moderation import target_issue


class ModerationCommands(commands.Cog):
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot

    async def send_error(self, interaction: discord.Interaction, message: str) -> None:
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="ping", description="Check whether the bot is responding")
    @app_commands.guild_only()
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Pong!", ephemeral=True)

    @app_commands.command(name="kick", description="Remove a member from this server")
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(member="The member to kick", reason="Why they are being kicked")
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ) -> None:
        problem = target_issue(interaction, member)
        if problem:
            await self.send_error(interaction, problem)
            return

        await interaction.response.defer(ephemeral=True)
        await member.kick(reason=reason)
        await interaction.followup.send(f"Kicked {member.mention}.", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from this server")
    @app_commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(member="The member to ban", reason="Why they are being banned")
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ) -> None:
        problem = target_issue(interaction, member)
        if problem:
            await self.send_error(interaction, problem)
            return

        await interaction.response.defer(ephemeral=True)
        await member.ban(reason=reason, delete_message_seconds=0)
        await interaction.followup.send(f"Banned {member.mention}.", ephemeral=True)

    @app_commands.command(name="timeout", description="Temporarily prevent a member from chatting")
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(
        member="The member to timeout",
        minutes="Duration, from 1 minute to 28 days",
        reason="Why they are being timed out",
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: app_commands.Range[int, 1, 40320],
        reason: str | None = None,
    ) -> None:
        problem = target_issue(interaction, member)
        if problem:
            await self.send_error(interaction, problem)
            return

        await interaction.response.defer(ephemeral=True)
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await interaction.followup.send(
            f"Timed out {member.mention} for {minutes} minute(s).", ephemeral=True
        )

    @app_commands.command(name="untimeout", description="Remove a member's timeout")
    @app_commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(member="The member to un-timeout", reason="Why the timeout is being removed")
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str | None = None,
    ) -> None:
        problem = target_issue(interaction, member)
        if problem:
            await self.send_error(interaction, problem)
            return

        await interaction.response.defer(ephemeral=True)
        await member.timeout(None, reason=reason)
        await interaction.followup.send(
            f"Removed {member.mention}'s timeout.", ephemeral=True
        )

    @app_commands.command(name="clear", description="Delete recent messages in this channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(amount="Number of recent messages to delete (1-100)")
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 1, 100],
    ) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await self.send_error(interaction, "Use this command in a server text channel.")
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await channel.purge(limit=amount)
        await interaction.followup.send(
            f"Deleted {len(deleted)} message(s).", ephemeral=True
        )

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            await self.send_error(interaction, "You don't have permission to use this command.")
            return

        original = error.original if isinstance(error, app_commands.CommandInvokeError) else error
        if isinstance(original, discord.Forbidden):
            message = "Discord denied that action. Check my permissions and role position."
        elif isinstance(original, discord.NotFound):
            message = "That member or message could not be found."
        else:
            message = "Something went wrong while running that command."
            logging.error(
                "Slash command failed",
                exc_info=(type(error), error, error.__traceback__),
            )

        await self.send_error(interaction, message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModerationCommands(bot))