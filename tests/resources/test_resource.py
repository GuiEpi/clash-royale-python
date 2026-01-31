from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from clash_royale.resources.resource import Resource


@pytest.fixture
def mock_client() -> MagicMock:
    """Return a mock client."""
    return MagicMock()


def test_base_resource_initialization(mock_client: MagicMock) -> None:
    """Test Resource initialization."""
    resource = Resource(client=mock_client)

    assert resource._client == mock_client


def test_base_resource_client_access(mock_client: MagicMock) -> None:
    """Test accessing the client from Resource."""
    resource = Resource(client=mock_client)

    # Should be able to access client
    assert resource._client is not None
    assert resource._client == mock_client


def test_base_resource_subclass() -> None:
    """Test creating a subclass of Resource."""
    mock_client = MagicMock()

    class TestResource(Resource):
        """Test resource subclass."""

        def test_method(self) -> str:
            """Test method."""
            return "test"

    resource = TestResource(client=mock_client)

    assert resource._client == mock_client
    assert resource.test_method() == "test"


def test_base_resource_client_methods(mock_client: MagicMock) -> None:
    """Test that resource can call client methods."""
    mock_client._request.return_value = {"data": "test"}

    resource = Resource(client=mock_client)

    # Resource should be able to call client methods
    result = resource._client._request("GET", "/test")

    assert result == {"data": "test"}
    mock_client._request.assert_called_once_with("GET", "/test")
