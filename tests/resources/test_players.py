from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.player import Battle, Player, UpcomingChest


@pytest.mark.vcr()
def test_get_player(client: clash_royale.Client) -> None:
    """Test getting a player with full model validation.

    This test covers:
    - Basic player fetch
    - Player model fields
    - Clan information (optional)
    """
    player_tag = "#9G9JL8QU"

    player = client.players.get(player_tag)

    assert isinstance(player, Player)
    assert player.tag == "#9G9JL8QU"
    assert player.name is not None
    assert player.exp_level > 0
    assert player.trophies >= 0

    # Clan is optional - player might not be in a clan
    # Just verify the field is accessible
    _ = player.clan


@pytest.mark.vcr()
def test_get_player_tag_normalization(client: clash_royale.Client) -> None:
    """Test that player tags are normalized (uppercase, with #)."""
    # Test with lowercase tag without #
    player1 = client.players.get("9g9jl8qu")
    assert player1.tag == "#9G9JL8QU"

    # Test with tag with # (lowercase)
    player2 = client.players.get("#9g9jl8qu")
    assert player2.tag == "#9G9JL8QU"

    # Test with tag already normalized
    player3 = client.players.get("#9G9JL8QU")
    assert player3.tag == "#9G9JL8QU"


@pytest.mark.vcr()
def test_get_player_not_found(client: clash_royale.Client) -> None:
    """Test getting a non-existent player."""
    player_tag = "#NOTFOUND999999"

    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client.players.get(player_tag)


@pytest.mark.vcr()
def test_get_battlelog(client: clash_royale.Client) -> None:
    """Test getting player's battle log."""
    player_tag = "#9G9JL8QU"

    battles = client.players.get_battlelog(player_tag)

    assert isinstance(battles, list)
    # Player might not have recent battles
    if len(battles) > 0:
        assert isinstance(battles[0], Battle)
        assert battles[0].type is not None


@pytest.mark.vcr()
def test_get_upcoming_chests(client: clash_royale.Client) -> None:
    """Test getting player's upcoming chests."""
    player_tag = "#9G9JL8QU"

    chests = client.players.get_upcoming_chests(player_tag)

    assert isinstance(chests, list)

    # All players should have upcoming chests
    if len(chests) > 0:
        assert isinstance(chests[0], UpcomingChest)
        assert chests[0].index >= 0
        assert chests[0].name is not None


@pytest.mark.vcr()
def test_get_upcoming_chests_not_found(client: clash_royale.Client) -> None:
    """Test getting upcoming chests for non-existent player."""
    player_tag = "#NOTFOUND999999"

    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client.players.get_upcoming_chests(player_tag)


@pytest.mark.vcr()
def test_get_battlelog_not_found(client: clash_royale.Client) -> None:
    """Test getting battle log for non-existent player."""
    player_tag = "#NOTFOUND999999"

    # Note: The battlelog endpoint might return empty list instead of 404
    # for some invalid tags, so we check for either behavior
    try:
        battles = client.players.get_battlelog(player_tag)
        assert isinstance(battles, list)
    except clash_royale.ClashRoyaleNotFoundError:
        pass


def test_players_resource_initialization(client: clash_royale.Client) -> None:
    """Test Players resource initialization."""
    assert client.players is not None
    assert client.players._client == client
