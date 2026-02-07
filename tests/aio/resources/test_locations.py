from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.aio.pagination import PaginatedList
from clash_royale.models.location import (
    ClanRanking,
    LeagueSeason,
    LeagueSeasonV2,
    Location,
    PlayerPathOfLegendRanking,
    PlayerRanking,
    PlayerSeasonRanking,
)

# Location IDs
GLOBAL_LOCATION_ID = 57000000
FRANCE_LOCATION_ID = 57000094
US_LOCATION_ID = 57000249


@pytest.mark.vcr()
async def test_list_locations(client: Client) -> None:
    """Test listing locations with full model validation."""
    locations = client.locations.list(limit=10, page_size=10)

    assert isinstance(locations, PaginatedList)

    location_list = await locations.all()
    assert len(location_list) == 10

    for location in location_list:
        assert isinstance(location, Location)
        assert location.name is not None
        assert location.id is not None


@pytest.mark.vcr()
async def test_get_location(client: Client) -> None:
    """Test getting a location by ID."""
    location = await client.locations.get(GLOBAL_LOCATION_ID)

    assert isinstance(location, Location)
    assert location.id == GLOBAL_LOCATION_ID
    assert location.name is not None


@pytest.mark.vcr()
async def test_get_location_not_found(client: Client) -> None:
    """Test getting a non-existent location."""
    with pytest.raises(clash_royale.ClashRoyaleBadRequestError):
        await client.locations.get(99999999)


@pytest.mark.vcr()
async def test_get_clan_rankings(client: Client) -> None:
    """Test getting clan rankings with full model validation."""
    rankings = client.locations.get_clan_rankings(
        GLOBAL_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, ClanRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None


@pytest.mark.vcr()
async def test_get_player_rankings(client: Client) -> None:
    """Test getting player rankings for a location."""
    rankings = client.locations.get_player_rankings(
        US_LOCATION_ID, limit=5, page_size=5
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    if len(ranking_list) > 0:
        assert isinstance(ranking_list[0], PlayerRanking)
        assert ranking_list[0].tag is not None
        assert ranking_list[0].name is not None
        assert ranking_list[0].rank is not None


@pytest.mark.vcr()
async def test_get_clan_war_rankings(client: Client) -> None:
    """Test getting clan war rankings for a location."""
    rankings = client.locations.get_clan_war_rankings(
        US_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, ClanRanking)
        assert ranking.tag is not None
        assert ranking.name is not None


@pytest.mark.vcr()
async def test_get_path_of_legend_rankings(client: Client) -> None:
    """Test getting Path of Legend player rankings."""
    rankings = client.locations.get_path_of_legend_player_rankings(
        FRANCE_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerPathOfLegendRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None
        assert ranking.elo_rating is not None


@pytest.mark.vcr()
async def test_get_path_of_legend_season_rankings(client: Client) -> None:
    """Test getting Path of Legend season rankings."""
    season_id = "2024-12"

    rankings = client.locations.get_path_of_legend_season_rankings(
        season_id, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerPathOfLegendRanking)
        assert ranking.tag is not None
        assert ranking.elo_rating is not None


@pytest.mark.vcr()
async def test_get_season_with_date_code(client: Client) -> None:
    """Test getting a specific season using a date-based code."""
    season_id = "2025-07"

    with pytest.warns(UserWarning, match="incomplete season data"):
        season = await client.locations.get_season(season_id)

    assert isinstance(season, LeagueSeason)
    assert season.id == season_id


@pytest.mark.vcr()
async def test_get_season_with_numeric_id(client: Client) -> None:
    """Test getting a specific season using a numeric unique ID."""
    season_id = "1"

    with pytest.warns(UserWarning, match="incomplete season data"):
        season = await client.locations.get_season(season_id)

    assert isinstance(season, LeagueSeasonV2)
    if season.unique_id is not None:
        assert season.unique_id == season_id


async def test_list_seasons(client: Client) -> None:
    """Test listing league seasons."""
    with pytest.warns(UserWarning, match="incomplete season data"):
        seasons = client.locations.list_seasons()

    assert isinstance(seasons, PaginatedList)


@pytest.mark.vcr()
async def test_list_seasons_v2(client: Client) -> None:
    """Test listing league seasons with v2 endpoint."""
    with pytest.warns(UserWarning, match="incomplete season data"):
        seasons = client.locations.list_seasons_v2()

    assert isinstance(seasons, PaginatedList)

    season_list = await seasons.slice(0, 10)
    assert len(season_list) <= 10

    for season in season_list:
        assert isinstance(season, LeagueSeasonV2)


@pytest.mark.vcr()
async def test_get_season_player_rankings(client: Client) -> None:
    """Test getting player rankings for a season."""
    season_id = "2017-03"

    rankings = client.locations.get_season_player_rankings(
        season_id, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = await rankings.all()
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerSeasonRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None
        assert ranking.trophies is not None


async def test_locations_resource_initialization(client: Client) -> None:
    """Test Locations resource initialization."""
    assert client.locations is not None
    assert client.locations._client == client
