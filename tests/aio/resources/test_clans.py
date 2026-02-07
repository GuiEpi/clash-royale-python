from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.aio.pagination import PaginatedList
from clash_royale.models.clan import Clan, ClanMember

# Known working clan tag
CLAN_TAG = "#2Q8CCP0"


@pytest.mark.vcr()
async def test_get_clan(client: Client) -> None:
    """Test getting a clan with full model validation."""
    clan = await client.clans.get(CLAN_TAG)

    assert isinstance(clan, Clan)
    assert clan.tag == "#2Q8CCP0"
    assert clan.name is not None
    assert isinstance(clan.members, int)


@pytest.mark.vcr()
async def test_get_clan_tag_normalization(client: Client) -> None:
    """Test that clan tags are normalized (uppercase, with #)."""
    clan1 = await client.clans.get("2q8ccp0")
    assert clan1.tag == "#2Q8CCP0"

    clan2 = await client.clans.get("#2q8ccp0")
    assert clan2.tag == "#2Q8CCP0"

    clan3 = await client.clans.get("#2Q8CCP0")
    assert clan3.tag == "#2Q8CCP0"


@pytest.mark.vcr()
async def test_get_clan_not_found(client: Client) -> None:
    """Test getting a non-existent clan."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client.clans.get("#NOTFOUND999999")


@pytest.mark.vcr()
async def test_search_clans(client: Client) -> None:
    """Test searching for clans with various parameters."""
    results = client.clans.search(name="Reddit", limit=5, page_size=5)

    assert isinstance(results, PaginatedList)

    clans = await results.all()
    assert len(clans) == 5
    assert any("reddit" in clan.name.lower() for clan in clans)

    # Search with min_members filter
    filtered_results = client.clans.search(
        name="Legend", min_members=40, limit=5, page_size=5
    )
    filtered_clans = await filtered_results.all()

    assert len(filtered_clans) == 5
    assert all(clan.members >= 40 for clan in filtered_clans)


@pytest.mark.vcr()
async def test_get_members(client: Client) -> None:
    """Test getting clan members with full model validation."""
    members = client.clans.get_members(CLAN_TAG, limit=10, page_size=10)

    assert isinstance(members, PaginatedList)

    members_list = await members.all()
    assert len(members_list) <= 10

    for member in members_list:
        assert isinstance(member, ClanMember)
        assert member.tag is not None
        assert member.name is not None


@pytest.mark.vcr()
async def test_get_current_river_race(client: Client) -> None:
    """Test getting current river race."""
    try:
        river_race = await client.clans.get_current_river_race(CLAN_TAG)
        assert river_race.clan.tag == "#2Q8CCP0"
    except clash_royale.ClashRoyaleNotFoundError:
        pytest.skip("River race not active for this clan")


@pytest.mark.vcr()
async def test_get_current_river_race_not_found(client: Client) -> None:
    """Test getting current river race for non-existent clan."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client.clans.get_current_river_race("#NOTFOUND999999")


@pytest.mark.vcr()
async def test_get_river_race_log(client: Client) -> None:
    """Test getting river race log."""
    log = client.clans.get_river_race_log(CLAN_TAG, limit=5, page_size=5)

    assert isinstance(log, PaginatedList)

    log_list = await log.all()
    assert len(log_list) <= 5


async def test_clans_resource_initialization(client: Client) -> None:
    """Test Clans resource initialization."""
    assert client.clans is not None
    assert client.clans._client == client
