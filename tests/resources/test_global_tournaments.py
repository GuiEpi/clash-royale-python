from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.global_tournament import GlobalTournament
from clash_royale.pagination import PaginatedList


@pytest.mark.vcr()
def test_list_global_tournaments(client: clash_royale.Client) -> None:
    """Test listing global tournaments with full model validation.

    This test covers:
    - Basic API call and PaginatedList behavior
    - Limit/page_size parameters
    - All GlobalTournament model fields
    - Nested objects (milestones, game_mode, rewards)
    """
    tournaments = client.global_tournaments.list(limit=5, page_size=5)

    assert isinstance(tournaments, PaginatedList)

    tournament_list = list(tournaments)
    assert isinstance(tournament_list, list)
    assert len(tournament_list) <= 5

    # Validate all tournaments are properly typed
    for tournament in tournament_list:
        assert isinstance(tournament, GlobalTournament)

    # If tournaments exist, validate structure
    if len(tournament_list) > 0:
        tournament = tournament_list[0]

        # Core fields
        assert tournament.tag is not None
        assert tournament.tag.startswith("#")
        assert tournament.tag == tournament.tag.upper()
        assert tournament.title is not None
        assert tournament.max_losses >= 0
        assert tournament.min_exp_level >= 0
        assert tournament.tournament_level >= 0

        # Time fields
        assert isinstance(tournament.start_time, str)
        assert isinstance(tournament.end_time, str)
        assert len(tournament.start_time) > 0
        assert len(tournament.end_time) > 0

        # Milestones (optional)
        if tournament.milestones:
            assert isinstance(tournament.milestones, list)
            if len(tournament.milestones) > 0:
                milestone = tournament.milestones[0]
                assert hasattr(milestone, "wins")
                assert hasattr(milestone, "type")
                assert milestone.wins >= 0

        # Game mode (optional)
        if tournament.game_mode is not None:
            assert hasattr(tournament.game_mode, "id")
            assert hasattr(tournament.game_mode, "name")
            assert tournament.game_mode.id > 0
            assert tournament.game_mode.name is not None

        # Rewards (optional, just verify accessible)
        _ = tournament.free_tier_rewards
        _ = tournament.top_rank_reward
        _ = tournament.max_top_reward_rank


@pytest.mark.vcr()
def test_list_global_tournaments_no_params(client: clash_royale.Client) -> None:
    """Test listing global tournaments without limit/page_size.

    Uses API defaults - may return empty list if no tournaments active.
    """
    tournaments = client.global_tournaments.list()

    assert isinstance(tournaments, PaginatedList)

    # Just fetch first few to avoid long iteration
    tournament_list = tournaments[:5]
    assert isinstance(tournament_list, list)


def test_globaltournaments_resource_initialization(client: clash_royale.Client) -> None:
    """Test GlobalTournaments resource initialization."""
    assert client.global_tournaments is not None
    assert client.global_tournaments._client == client
