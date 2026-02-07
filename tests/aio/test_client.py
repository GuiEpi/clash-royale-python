from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client


async def test_client_initialization(client: Client, api_key: str) -> None:
    """Test async client initialization."""
    assert client._auth.api_key == api_key
    assert client.players is not None
    assert client.clans is not None
    assert client.cards is not None
    assert client.locations is not None
    assert client.tournaments is not None
    assert client.global_tournaments is not None
    assert client.leaderboards is not None


async def test_client_context_manager(api_key: str) -> None:
    """Test async client as context manager."""
    async with Client(api_key=api_key, proxy="https://proxy.royaleapi.dev") as client:
        assert client is not None


@pytest.mark.vcr()
async def test_unauthorized_error() -> None:
    """Test unauthorized error with invalid API key."""
    client = Client(api_key="invalid_key_12345")

    with pytest.raises(clash_royale.ClashRoyaleUnauthorizedError):
        await client.players.get("#9G9JL8QU")

    await client.aclose()


def test_empty_api_key() -> None:
    """Test that creating an async client with an empty API key raises an error."""
    with pytest.raises(clash_royale.InvalidAPIKeyError):
        Client(api_key="")


@pytest.mark.vcr()
async def test_request_method_get(client: Client) -> None:
    """Test async request method with GET request."""
    response = await client._request("GET", "/players/%239G9JL8QU")

    assert isinstance(response, dict)
    assert "tag" in response
    assert response["tag"] == "#9G9JL8QU"


@pytest.mark.vcr()
async def test_request_method_with_params(client: Client) -> None:
    """Test async request method with query parameters."""
    response = await client._request(
        "GET", "/clans/%232Q8CCP0/members", params={"limit": 5}
    )

    assert isinstance(response, dict)
    assert "items" in response


@pytest.mark.vcr()
async def test_request_method_not_found(client: Client) -> None:
    """Test async request method raises ClashRoyaleNotFoundError for 404."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        await client._request("GET", "/players/invalid_tag_format")


@pytest.mark.vcr()
async def test_request_method_bad__request(client: Client) -> None:
    """Test async request method raises ClashRoyaleBadRequestError for 400."""
    with pytest.raises(clash_royale.ClashRoyaleBadRequestError):
        await client._request("GET", "/tournaments")


async def test_convert_params_to_camel_case(client: Client) -> None:
    """Test parameter conversion from snake_case to camelCase."""
    # Test single underscore
    params = {"min_members": 40}
    result = client._convert_params_to_camel_case(params)
    assert result == {"minMembers": 40}

    # Test multiple underscores
    params = {"location_id": 123, "max_score": 5000}
    result = client._convert_params_to_camel_case(params)
    assert result == {"locationId": 123, "maxScore": 5000}

    # Test no underscores (should remain unchanged)
    params = {"name": "Legend", "limit": 10}
    result = client._convert_params_to_camel_case(params)
    assert result == {"name": "Legend", "limit": 10}

    # Test mixed parameters
    params = {"name": "Test", "min_members": 40, "max_members": 50, "limit": 100}
    result = client._convert_params_to_camel_case(params)
    assert result == {
        "name": "Test",
        "minMembers": 40,
        "maxMembers": 50,
        "limit": 100,
    }

    # Test multiple words with underscores
    params = {"some_long_parameter_name": "value"}
    result = client._convert_params_to_camel_case(params)
    assert result == {"someLongParameterName": "value"}


@pytest.mark.vcr()
async def test_request_with_snake_case_params(client: Client) -> None:
    """Test that snake_case parameters are properly converted in actual requests."""
    response = await client._request(
        "GET", "/clans", params={"name": "Legend", "min_members": 40, "limit": 5}
    )

    assert isinstance(response, dict)
    assert "items" in response
    clans = response.get("items", [])
    if len(clans) > 0:
        assert all(clan["members"] >= 40 for clan in clans)
