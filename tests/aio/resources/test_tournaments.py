from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.aio.pagination import PaginatedList
from clash_royale.models.tournament import Tournament, TournamentHeader


@pytest.mark.vcr()
async def test_get_tournament(client: Client) -> None:
    """Test getting a tournament by tag."""
    tournament_tag = "#2PP"

    tournament = await client.tournaments.get(tournament_tag)

    assert isinstance(tournament, Tournament)
    assert tournament.tag.upper() == tournament_tag.upper()
    assert tournament.name is not None


@pytest.mark.vcr()
async def test_get_tournament_tag_normalization(client: Client) -> None:
    """Test that tournament tags are normalized (uppercase, with #)."""
    tournament_tag = "2pp"

    tournament = await client.tournaments.get(tournament_tag)
    assert tournament.tag == "#2PP"
    assert tournament.tag.startswith("#")


@pytest.mark.vcr()
async def test_get_tournament_not_found(client: Client) -> None:
    """Test getting a non-existent tournament."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client.tournaments.get("#NOTFOUND999999")


@pytest.mark.vcr()
async def test_search_tournaments(client: Client) -> None:
    """Test searching for tournaments with various parameters."""
    results = client.tournaments.search(name="Test", limit=5, page_size=5)

    assert isinstance(results, PaginatedList)

    tournaments = await results.all()
    assert len(tournaments) <= 5

    for tournament in tournaments:
        assert isinstance(tournament, TournamentHeader)
        assert tournament.tag is not None
        assert tournament.name is not None


async def test_tournaments_resource_initialization(client: Client) -> None:
    """Test Tournaments resource initialization."""
    assert client.tournaments is not None
    assert client.tournaments._client == client
