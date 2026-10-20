import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import discord
from services.moderation import target_issue


class DummyUser:
    def __init__(self, user_id):
        self.id = user_id


class DummyMember(DummyUser):
    def __init__(self, user_id, top_role):
        super().__init__(user_id)
        self.top_role = top_role


class DummyGuild:
    def __init__(self, owner_id, bot_top_role):
        self.owner_id = owner_id
        self.me = DummyMember(999, bot_top_role)


class DummyClient:
    def __init__(self, bot_id):
        self.user = DummyUser(bot_id)


class DummyInteraction:
    def __init__(self, guild, actor, bot_id=999):
        self.guild = guild
        self.user = actor
        self.client = DummyClient(bot_id)


@pytest.fixture
def fake_discord_member(monkeypatch):
    monkeypatch.setattr(discord, "Member", DummyMember)


def test_valid_target_returns_none(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=50)
    actor = DummyMember(100, 20)
    target = DummyMember(101, 10)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) is None


def test_rejects_self_moderation(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=50)
    actor = DummyMember(100, 20)
    target = DummyMember(100, 10)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) == "You cannot moderate yourself."


def test_rejects_bot_target(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=50)
    actor = DummyMember(100, 20)
    target = DummyMember(999, 10)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) == "I cannot moderate myself."


def test_rejects_server_owner_target(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=50)
    actor = DummyMember(100, 20)
    target = DummyMember(200, 10)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) == "The server owner cannot be moderated by this bot."


def test_rejects_member_above_actor_role(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=50)
    actor = DummyMember(100, 20)
    target = DummyMember(101, 25)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) == "You can only moderate members whose highest role is below yours."


def test_rejects_target_above_bot_role(fake_discord_member):
    guild = DummyGuild(owner_id=200, bot_top_role=20)
    actor = DummyMember(100, 30)
    target = DummyMember(101, 25)
    interaction = DummyInteraction(guild, actor)

    assert target_issue(interaction, target) == "My highest role must be above the target's highest role."


def test_rejects_non_guild_context(fake_discord_member):
    actor = object()
    target = DummyMember(101, 10)

    interaction = DummyInteraction(guild=None, actor=actor)

    assert target_issue(interaction, target) == "This command can only be used in a server."
