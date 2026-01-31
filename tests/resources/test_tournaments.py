from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.tournament import Tournament, TournamentHeader
from clash_royale.pagination import PaginatedList


@pytest.mark.vcr()
def test_get_tournament(client: clash_royale.Client) -> None:
    """Test getting a tournament by tag."""
    tournament_tag = "#2PP"

    tournament = client.tournaments.get(tournament_tag)

    assert isinstance(tournament, Tournament)
    assert tournament.tag.upper() == tournament_tag.upper()
    assert tournament.name is not None


@pytest.mark.vcr()
def test_get_tournament_tag_normalization(client: clash_royale.Client) -> None:
    """Test that tournament tags are normalized (uppercase, with #)."""
    tournament_tag = "2pp"

    # Test with lowercase tag without # - should normalize to uppercase with #
    tournament = client.tournaments.get(tournament_tag)
    assert tournament.tag == "#2PP"
    assert tournament.tag.startswith("#")


@pytest.mark.vcr()
def test_get_tournament_not_found(client: clash_royale.Client) -> None:
    """Test getting a non-existent tournament."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client.tournaments.get("#NOTFOUND999999")


@pytest.mark.vcr()
def test_search_tournaments(client: clash_royale.Client) -> None:
    """Test searching for tournaments with various parameters.

    This test covers:
    - Basic tournament search
    - Limit/page_size parameters
    """
    results = client.tournaments.search(name="Test", limit=5, page_size=5)

    assert isinstance(results, PaginatedList)

    tournaments = list(results)
    # There might or might not be tournaments with this name
    assert len(tournaments) <= 5

    for tournament in tournaments:
        assert isinstance(tournament, TournamentHeader)
        assert tournament.tag is not None
        assert tournament.name is not None


def test_tournaments_resource_initialization(client: clash_royale.Client) -> None:
    """Test Tournaments resource initialization."""
    assert client.tournaments is not None
    assert client.tournaments._client == client
