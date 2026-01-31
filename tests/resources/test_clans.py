from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.clan import Clan, ClanMember
from clash_royale.pagination import PaginatedList

# Known working clan tag
CLAN_TAG = "#2Q8CCP0"


@pytest.mark.vcr()
def test_get_clan(client: clash_royale.Client) -> None:
    """Test getting a clan with full model validation."""
    clan = client.clans.get(CLAN_TAG)

    assert isinstance(clan, Clan)
    assert clan.tag == "#2Q8CCP0"
    assert clan.name is not None
    assert isinstance(clan.members, int)


@pytest.mark.vcr()
def test_get_clan_tag_normalization(client: clash_royale.Client) -> None:
    """Test that clan tags are normalized (uppercase, with #)."""
    # Test with lowercase tag without #
    clan1 = client.clans.get("2q8ccp0")
    assert clan1.tag == "#2Q8CCP0"

    # Test with tag with # (lowercase)
    clan2 = client.clans.get("#2q8ccp0")
    assert clan2.tag == "#2Q8CCP0"

    # Test with tag already normalized
    clan3 = client.clans.get("#2Q8CCP0")
    assert clan3.tag == "#2Q8CCP0"


@pytest.mark.vcr()
def test_get_clan_not_found(client: clash_royale.Client) -> None:
    """Test getting a non-existent clan."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client.clans.get("#NOTFOUND999999")


@pytest.mark.vcr()
def test_search_clans(client: clash_royale.Client) -> None:
    """Test searching for clans with various parameters.

    This test covers:
    - Basic clan search
    - Search with filters (min_members)
    - Limit/page_size parameters
    """
    # Basic search
    results = client.clans.search(name="Reddit", limit=5, page_size=5)

    assert isinstance(results, PaginatedList)

    clans = list(results)
    assert len(clans) == 5
    assert any("reddit" in clan.name.lower() for clan in clans)

    # Search with min_members filter
    filtered_results = client.clans.search(
        name="Legend", min_members=40, limit=5, page_size=5
    )
    filtered_clans = list(filtered_results)

    assert len(filtered_clans) == 5
    assert all(clan.members >= 40 for clan in filtered_clans)


@pytest.mark.vcr()
def test_get_members(client: clash_royale.Client) -> None:
    """Test getting clan members with full model validation."""
    members = client.clans.get_members(CLAN_TAG, limit=10, page_size=10)

    assert isinstance(members, PaginatedList)

    members_list = list(members)
    assert len(members_list) <= 10

    for member in members_list:
        assert isinstance(member, ClanMember)
        assert member.tag is not None
        assert member.name is not None


@pytest.mark.vcr()
def test_get_current_river_race(client: clash_royale.Client) -> None:
    """Test getting current river race."""
    try:
        river_race = client.clans.get_current_river_race(CLAN_TAG)
        # If successful, verify the structure
        assert river_race.clan.tag == "#2Q8CCP0"
    except clash_royale.ClashRoyaleNotFoundError:
        # River race might not be active
        pytest.skip("River race not active for this clan")


@pytest.mark.vcr()
def test_get_current_river_race_not_found(client: clash_royale.Client) -> None:
    """Test getting current river race for non-existent clan."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client.clans.get_current_river_race("#NOTFOUND999999")


@pytest.mark.vcr()
def test_get_river_race_log(client: clash_royale.Client) -> None:
    """Test getting river race log."""
    log = client.clans.get_river_race_log(CLAN_TAG, limit=5, page_size=5)

    assert isinstance(log, PaginatedList)

    log_list = list(log)
    assert len(log_list) <= 5


def test_clans_resource_initialization(client: clash_royale.Client) -> None:
    """Test Clans resource initialization."""
    assert client.clans is not None
    assert client.clans._client == client
