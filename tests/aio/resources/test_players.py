from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.models.player import Battle, Player, UpcomingChest


@pytest.mark.vcr()
async def test_get_player(client: Client) -> None:
    """Test getting a player with full model validation."""
    player_tag = "#9G9JL8QU"

    player = await client.players.get(player_tag)

    assert isinstance(player, Player)
    assert player.tag == "#9G9JL8QU"
    assert player.name is not None
    assert player.exp_level > 0
    assert player.trophies >= 0

    _ = player.clan


@pytest.mark.vcr()
async def test_get_player_tag_normalization(client: Client) -> None:
    """Test that player tags are normalized (uppercase, with #)."""
    player1 = await client.players.get("9g9jl8qu")
    assert player1.tag == "#9G9JL8QU"

    player2 = await client.players.get("#9g9jl8qu")
    assert player2.tag == "#9G9JL8QU"

    player3 = await client.players.get("#9G9JL8QU")
    assert player3.tag == "#9G9JL8QU"


@pytest.mark.vcr()
async def test_get_player_not_found(client: Client) -> None:
    """Test getting a non-existent player."""
    player_tag = "#NOTFOUND999999"

    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client.players.get(player_tag)


@pytest.mark.vcr()
async def test_get_battlelog(client: Client) -> None:
    """Test getting player's battle log."""
    player_tag = "#9G9JL8QU"

    battles = await client.players.get_battlelog(player_tag)

    assert isinstance(battles, list)
    if len(battles) > 0:
        assert isinstance(battles[0], Battle)
        assert battles[0].type is not None


@pytest.mark.vcr()
async def test_get_upcoming_chests(client: Client) -> None:
    """Test getting player's upcoming chests."""
    player_tag = "#9G9JL8QU"

    chests = await client.players.get_upcoming_chests(player_tag)

    assert isinstance(chests, list)

    if len(chests) > 0:
        assert isinstance(chests[0], UpcomingChest)
        assert chests[0].index >= 0
        assert chests[0].name is not None


@pytest.mark.vcr()
async def test_get_upcoming_chests_not_found(client: Client) -> None:
    """Test getting upcoming chests for non-existent player."""
    player_tag = "#NOTFOUND999999"

    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client.players.get_upcoming_chests(player_tag)


@pytest.mark.vcr()
async def test_get_battlelog_not_found(client: Client) -> None:
    """Test getting battle log for non-existent player."""
    player_tag = "#NOTFOUND999999"

    try:
        battles = await client.players.get_battlelog(player_tag)
        assert isinstance(battles, list)
    except clash_royale.ClashRoyaleNotFoundError:
        pass


async def test_players_resource_initialization(client: Client) -> None:
    """Test Players resource initialization."""
    assert client.players is not None
    assert client.players._client == client
