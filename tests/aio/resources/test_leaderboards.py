from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.aio.pagination import PaginatedList
from clash_royale.models.leaderboard import Leaderboard, LeaderboardPlayer

# Known working leaderboard ID
LEADERBOARD_ID = 170000008


@pytest.mark.vcr()
async def test_list_leaderboards(client: Client) -> None:
    """Test listing all available leaderboards."""
    leaderboards = await client.leaderboards.list()

    assert isinstance(leaderboards, list)
    assert len(leaderboards) > 0
    assert isinstance(leaderboards[0], Leaderboard)
    assert leaderboards[0].id is not None
    assert leaderboards[0].name is not None


@pytest.mark.vcr()
async def test_get_leaderboard(client: Client) -> None:
    """Test getting a leaderboard with full model validation."""
    players = client.leaderboards.get(LEADERBOARD_ID, limit=10, page_size=10)

    assert isinstance(players, PaginatedList)

    player_list = await players.all()
    assert len(player_list) == 10

    for player in player_list:
        assert isinstance(player, LeaderboardPlayer)
        assert player.tag is not None
        assert player.name is not None
        assert player.rank is not None
        assert player.score is not None
        assert player.score >= 0
        assert isinstance(player.score, int)
        _ = player.clan

    # Validate ranking order (ascending)
    for i in range(len(player_list) - 1):
        assert player_list[i].rank <= player_list[i + 1].rank

    # Top player should be rank 1
    assert player_list[0].rank == 1


@pytest.mark.vcr()
async def test_get_leaderboard_pagination(client: Client) -> None:
    """Test paginated leaderboard results across multiple pages."""
    players = client.leaderboards.get(LEADERBOARD_ID, limit=25, page_size=10)

    player_list = await players.all()

    assert len(player_list) == 25
    assert all(isinstance(p, LeaderboardPlayer) for p in player_list)


@pytest.mark.vcr()
async def test_get_leaderboard_not_found(client: Client) -> None:
    """Test getting a non-existent leaderboard."""
    leaderboard_id = 99999999

    players = client.leaderboards.get(leaderboard_id)

    with pytest.raises(
        (
            clash_royale.ClashRoyaleNotFoundError,
            clash_royale.ClashRoyaleBadRequestError,
            clash_royale.ClashRoyaleServerError,
        )
    ):
        await players.get(0)


async def test_leaderboards_resource_initialization(client: Client) -> None:
    """Test Leaderboards resource initialization."""
    assert client.leaderboards is not None
    assert client.leaderboards._client == client
