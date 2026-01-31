from __future__ import annotations

import pytest

import clash_royale


def test_client_initialization(client: clash_royale.Client, api_key: str) -> None:
    """Test client initialization."""
    assert client._auth.api_key == api_key
    assert client.players is not None
    assert client.clans is not None
    assert client.cards is not None
    assert client.locations is not None
    assert client.tournaments is not None
    assert client.global_tournaments is not None
    assert client.leaderboards is not None


def test_client_context_manager(client: clash_royale.Client) -> None:
    """Test client as context manager."""
    with client:
        assert client is not None


@pytest.mark.vcr()
def test_unauthorized_error() -> None:
    """Test unauthorized error with invalid API key."""
    # Use obviously invalid API key
    client = clash_royale.Client(api_key="invalid_key_12345")

    with pytest.raises(clash_royale.ClashRoyaleUnauthorizedError):
        client.players.get("#9G9JL8QU")


def test_empty_api_key() -> None:
    """Test that creating a client with an empty API key raises an error."""
    with pytest.raises(clash_royale.InvalidAPIKeyError):
        clash_royale.Client(api_key="")


@pytest.mark.vcr()
def test_request_method_get(client: clash_royale.Client) -> None:
    """Test request method with GET request."""
    # Test a simple GET request
    response = client._request("GET", "/players/%239G9JL8QU")

    assert isinstance(response, dict)
    assert "tag" in response
    assert response["tag"] == "#9G9JL8QU"


@pytest.mark.vcr()
def test_request_method_with_params(client: clash_royale.Client) -> None:
    """Test request method with query parameters."""
    # Test request with limit parameter
    response = client._request("GET", "/clans/%232Q8CCP0/members", params={"limit": 5})

    assert isinstance(response, dict)
    assert "items" in response


@pytest.mark.vcr()
def test_request_method_not_found(client: clash_royale.Client) -> None:
    """Test request method raises ClashRoyaleNotFoundError for 404."""
    with pytest.raises(clash_royale.ClashRoyaleNotFoundError):
        client._request("GET", "/players/invalid_tag_format")


@pytest.mark.vcr()
def test_request_method_bad__request(client: clash_royale.Client) -> None:
    """Test request method raises ClashRoyaleBadRequestError for 400."""
    with pytest.raises(clash_royale.ClashRoyaleBadRequestError):
        client._request("GET", "/tournaments")


def test_convert_params_to_camel_case(client: clash_royale.Client) -> None:
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
def test_request_with_snake_case_params(client: clash_royale.Client) -> None:
    """Test that snake_case parameters are properly converted in actual requests."""
    # Search for clans with min_members parameter (snake_case)
    # This should be converted to minMembers (camelCase) for the API
    response = client._request(
        "GET", "/clans", params={"name": "Legend", "min_members": 40, "limit": 5}
    )

    assert isinstance(response, dict)
    assert "items" in response
    # Verify that clans returned respect the minMembers filter
    clans = response.get("items", [])
    if len(clans) > 0:
        # All clans should have at least 40 members
        assert all(clan["members"] >= 40 for clan in clans)
