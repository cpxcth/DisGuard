import discord


def target_issue(interaction: discord.Interaction, target: discord.Member) -> str | None:
    guild = interaction.guild
    actor = interaction.user
    bot_member = guild.me if guild else None

    if guild is None or not isinstance(actor, discord.Member) or bot_member is None:
        return "This command can only be used in a server."
    if target.id == actor.id:
        return "You cannot moderate yourself."
    if interaction.client.user and target.id == interaction.client.user.id:
        return "I cannot moderate myself."
    if target.id == guild.owner_id:
        return "The server owner cannot be moderated by this bot."
    if actor.id != guild.owner_id and target.top_role >= actor.top_role:
        return "You can only moderate members whose highest role is below yours."
    if target.top_role >= bot_member.top_role:
        return "My highest role must be above the target's highest role."
    return None