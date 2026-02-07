from __future__ import annotations

from unittest.mock import MagicMock

from clash_royale.aio.resources.resource import Resource


def test_base_resource_initialization() -> None:
    """Test async Resource initialization."""
    mock_client = MagicMock()
    resource = Resource(client=mock_client)

    assert resource._client == mock_client


def test_base_resource_client_access() -> None:
    """Test accessing the client from async Resource."""
    mock_client = MagicMock()
    resource = Resource(client=mock_client)

    assert resource._client is not None
    assert resource._client == mock_client


def test_base_resource_subclass() -> None:
    """Test creating a subclass of async Resource."""
    mock_client = MagicMock()

    class TestResource(Resource):
        """Test resource subclass."""

        def test_method(self) -> str:
            """Test method."""
            return "test"

    resource = TestResource(client=mock_client)

    assert resource._client == mock_client
    assert resource.test_method() == "test"


def test_base_resource_tag_normalization() -> None:
    """Test tag normalization and encoding."""
    mock_client = MagicMock()
    resource = Resource(client=mock_client)

    # Normalize tags
    assert resource._normalize_tag("abc") == "#ABC"
    assert resource._normalize_tag("#abc") == "#ABC"
    assert resource._normalize_tag("#ABC") == "#ABC"

    # Encode tags (URL encoding)
    encoded = resource._encode_tag("abc")
    assert "%23" in encoded  # # is encoded as %23
