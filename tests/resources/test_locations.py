from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.location import (
    ClanRanking,
    LeagueSeason,
    LeagueSeasonV2,
    Location,
    PlayerPathOfLegendRanking,
    PlayerRanking,
    PlayerSeasonRanking,
)
from clash_royale.pagination import PaginatedList

# Location IDs
GLOBAL_LOCATION_ID = 57000000
FRANCE_LOCATION_ID = 57000094
US_LOCATION_ID = 57000249


@pytest.mark.vcr()
def test_list_locations(client: clash_royale.Client) -> None:
    """Test listing locations with full model validation."""
    locations = client.locations.list(limit=10, page_size=10)

    assert isinstance(locations, PaginatedList)

    location_list = list(locations)
    assert len(location_list) == 10

    for location in location_list:
        assert isinstance(location, Location)
        assert location.name is not None
        assert location.id is not None


@pytest.mark.vcr()
def test_get_location(client: clash_royale.Client) -> None:
    """Test getting a location by ID."""
    location = client.locations.get(GLOBAL_LOCATION_ID)

    assert isinstance(location, Location)
    assert location.id == GLOBAL_LOCATION_ID
    assert location.name is not None


@pytest.mark.vcr()
def test_get_location_not_found(client: clash_royale.Client) -> None:
    """Test getting a non-existent location."""
    with pytest.raises(clash_royale.ClashRoyaleBadRequestError):
        client.locations.get(99999999)


@pytest.mark.vcr()
def test_get_clan_rankings(client: clash_royale.Client) -> None:
    """Test getting clan rankings with full model validation.

    This test covers:
    - Clan rankings for a location
    - ClanRanking model fields
    - Ranking order validation
    """
    rankings = client.locations.get_clan_rankings(
        GLOBAL_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, ClanRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None


@pytest.mark.vcr()
def test_get_player_rankings(client: clash_royale.Client) -> None:
    """Test getting player rankings for a location."""
    rankings = client.locations.get_player_rankings(
        US_LOCATION_ID, limit=5, page_size=5
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    if len(ranking_list) > 0:
        assert isinstance(ranking_list[0], PlayerRanking)
        assert ranking_list[0].tag is not None
        assert ranking_list[0].name is not None
        assert ranking_list[0].rank is not None


@pytest.mark.vcr()
def test_get_clan_war_rankings(client: clash_royale.Client) -> None:
    """Test getting clan war rankings for a location."""
    rankings = client.locations.get_clan_war_rankings(
        US_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, ClanRanking)
        assert ranking.tag is not None
        assert ranking.name is not None


@pytest.mark.vcr()
def test_get_path_of_legend_rankings(client: clash_royale.Client) -> None:
    """Test getting Path of Legend player rankings.

    This test covers:
    - Path of Legend rankings by location
    - PlayerPathOfLegendRanking model fields
    """
    rankings = client.locations.get_path_of_legend_player_rankings(
        FRANCE_LOCATION_ID, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerPathOfLegendRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None
        assert ranking.elo_rating is not None


@pytest.mark.vcr()
def test_get_path_of_legend_season_rankings(client: clash_royale.Client) -> None:
    """Test getting Path of Legend season rankings."""
    season_id = "2024-12"

    rankings = client.locations.get_path_of_legend_season_rankings(
        season_id, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerPathOfLegendRanking)
        assert ranking.tag is not None
        assert ranking.elo_rating is not None


@pytest.mark.vcr()
def test_get_season_with_date_code(client: clash_royale.Client) -> None:
    """Test getting a specific season using a date-based code.

    When season_id is a date-based code (e.g., "2025-07"), the legacy
    endpoint is used and returns a LeagueSeason.
    """
    season_id = "2025-07"

    season = client.locations.get_season(season_id)

    assert isinstance(season, LeagueSeason)
    assert season.id == season_id


@pytest.mark.vcr()
def test_get_season_with_numeric_id(client: clash_royale.Client) -> None:
    """Test getting a specific season using a numeric unique ID.

    When season_id is numeric (e.g., "1"), the V2 endpoint is used
    and returns a LeagueSeasonV2.
    """
    season_id = "1"

    season = client.locations.get_season(season_id)

    assert isinstance(season, LeagueSeasonV2)
    assert season.unique_id == season_id


def test_list_seasons(client: clash_royale.Client) -> None:
    """Test listing league seasons.

    Note: This endpoint returns incomplete data (null IDs) and emits a
    DeprecationWarning directing users to list_seasons_v2().
    We only verify the warning is raised and the return type is correct,
    without actually fetching data from the broken endpoint.
    """
    with pytest.warns(DeprecationWarning, match="use list_seasons_v2"):
        seasons = client.locations.list_seasons()

    assert isinstance(seasons, PaginatedList)


@pytest.mark.vcr()
def test_list_seasons_v2(client: clash_royale.Client) -> None:
    """Test listing league seasons with v2 endpoint."""
    seasons = client.locations.list_seasons_v2()

    assert isinstance(seasons, PaginatedList)

    season_list = seasons[:10]
    assert len(season_list) <= 10

    for season in season_list:
        assert isinstance(season, LeagueSeasonV2)


@pytest.mark.vcr()
def test_get_season_player_rankings(client: clash_royale.Client) -> None:
    """Test getting player rankings for a season."""
    season_id = "2017-03"

    rankings = client.locations.get_season_player_rankings(
        season_id, limit=10, page_size=10
    )

    assert isinstance(rankings, PaginatedList)

    ranking_list = list(rankings)
    assert len(ranking_list) == 10

    for ranking in ranking_list:
        assert isinstance(ranking, PlayerSeasonRanking)
        assert ranking.tag is not None
        assert ranking.name is not None
        assert ranking.rank is not None
        assert ranking.trophies is not None


def test_locations_resource_initialization(client: clash_royale.Client) -> None:
    """Test Locations resource initialization."""
    assert client.locations is not None
    assert client.locations._client == client
