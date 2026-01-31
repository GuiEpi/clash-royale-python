from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from clash_royale.pagination import PaginatedList


class MockModel(BaseModel):
    """Mock Pydantic model for testing."""

    id: int
    name: str


@pytest.fixture
def mock_client() -> MagicMock:
    """Return a mock client."""
    return MagicMock()


def test_paginated_list_initialization(mock_client: MagicMock) -> None:
    """Test PaginatedList initialization."""
    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"name": "test", "limit": 50, "page_size": 25},  # ty:ignore[invalid-argument-type]
    )

    assert paginated._client == mock_client
    assert paginated._endpoint == "/test"
    assert paginated._model == MockModel
    assert paginated._params == {"name": "test"}  # limit and page_size extracted
    assert paginated._limit == 50
    assert paginated._page_size == 25
    assert paginated._elements == []
    assert paginated._after_cursor is None
    assert paginated._has_more is True


def test_paginated_list_fetch_single_page(mock_client: MagicMock) -> None:
    """Test fetching a single page."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"page_size": 100},
    )

    items = list(paginated)

    assert len(items) == 2
    assert items[0].id == 1
    assert items[0].name == "Item 1"
    assert items[1].id == 2
    assert items[1].name == "Item 2"
    assert paginated._has_more is False

    # Verify page_size was sent as "limit" to API
    mock_client._request.assert_called_once_with("GET", "/test", params={"limit": 100})


def test_paginated_list_fetch_multiple_pages(mock_client: MagicMock) -> None:
    """Test fetching multiple pages."""
    # First page
    page1 = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    # Second page
    page2 = {
        "items": [{"id": 2, "name": "Item 2"}],
        "paging": {"cursors": {"after": "cursor2"}},
    }

    # Third page (last)
    page3 = {
        "items": [{"id": 3, "name": "Item 3"}],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2, page3]

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"page_size": 100},
    )

    items = list(paginated)

    assert len(items) == 3
    assert items[0].id == 1
    assert items[1].id == 2
    assert items[2].id == 3
    assert paginated._has_more is False

    # Verify correct number of requests and cursor usage
    assert mock_client._request.call_count == 3
    mock_client._request.assert_any_call("GET", "/test", params={"limit": 100})
    mock_client._request.assert_any_call(
        "GET", "/test", params={"after": "cursor1", "limit": 100}
    )
    mock_client._request.assert_any_call(
        "GET", "/test", params={"after": "cursor2", "limit": 100}
    )


def test_paginated_list_index_access(mock_client: MagicMock) -> None:
    """Test accessing items by index."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Access first item
    first = paginated[0]
    assert first.id == 1
    assert first.name == "Item 1"

    # Access second item
    second = paginated[1]
    assert second.id == 2

    # Access last item
    third = paginated[2]
    assert third.id == 3


def test_paginated_list_slice_access(mock_client: MagicMock) -> None:
    """Test accessing items by slice."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
            {"id": 4, "name": "Item 4"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Slice first 2 items
    first_two = paginated[:2]
    assert len(first_two) == 2
    assert first_two[0].id == 1
    assert first_two[1].id == 2

    # Slice middle items
    middle = paginated[1:3]
    assert len(middle) == 2
    assert middle[0].id == 2
    assert middle[1].id == 3

    # Slice with step
    every_other = paginated[::2]
    assert len(every_other) == 2
    assert every_other[0].id == 1
    assert every_other[1].id == 3


def test_paginated_list_lazy_loading_index(mock_client: MagicMock) -> None:
    """Test lazy loading when accessing by index."""
    page1 = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": 2, "name": "Item 2"}],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2]

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Access second item should trigger fetching page 2
    second = paginated[1]
    assert second.id == 2

    # Should have made 2 requests
    assert mock_client._request.call_count == 2


def test_paginated_list_lazy_loading_slice(mock_client: MagicMock) -> None:
    """Test lazy loading when accessing by slice."""
    page1 = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": 2, "name": "Item 2"}],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2]

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Slice [:2] should fetch both pages
    first_two = paginated[:2]
    assert len(first_two) == 2

    # Should have made 2 requests
    assert mock_client._request.call_count == 2


def test_paginated_list_repr(mock_client: MagicMock) -> None:
    """Test PaginatedList repr."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Repr should show first 5 items
    repr_str = repr(paginated)
    assert repr_str.startswith("<PaginatedList")


def test_paginated_list_repr_long_list(mock_client: MagicMock) -> None:
    """Test PaginatedList repr with long list."""
    page1 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 6)],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(6, 11)],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2]

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Repr should show first 5 items and "..."
    repr_str = repr(paginated)
    assert "..." in repr_str


def test_paginated_list_next(mock_client: MagicMock) -> None:
    """Test __next__ method."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Use next() to get items
    first = next(paginated)
    assert first.id == 1

    second = next(paginated)
    assert second.id == 2

    # Should raise StopIteration when exhausted
    with pytest.raises(StopIteration):
        next(paginated)


def test_paginated_list_with_params(mock_client: MagicMock) -> None:
    """Test PaginatedList with custom parameters."""
    mock_client._request.return_value = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"name": "test", "page_size": 10},  # ty:ignore[invalid-argument-type]
    )

    # Consume the list
    list(paginated)

    # Check that params were passed with page_size as "limit"
    mock_client._request.assert_called_once_with(
        "GET", "/test", params={"name": "test", "limit": 10}
    )


def test_paginated_list_empty_response(mock_client: MagicMock) -> None:
    """Test PaginatedList with empty response."""
    mock_client._request.return_value = {
        "items": [],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    items = list(paginated)

    assert len(items) == 0
    assert paginated._has_more is False


def test_paginated_list_fetch_all(mock_client: MagicMock) -> None:
    """Test _fetch_all method."""
    page1 = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": 2, "name": "Item 2"}],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2]

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Slice with no stop should fetch all
    all_items = paginated[:]

    assert len(all_items) == 2
    assert paginated._has_more is False
    assert mock_client._request.call_count == 2


def test_paginated_list_negative_index(mock_client: MagicMock) -> None:
    """Test accessing items with negative index."""
    mock_client._request.return_value = {
        "items": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
    )

    # Fetch all items first (negative indexing requires full list)
    all_items = list(paginated)

    # Now negative indexing should work
    last = all_items[-1]
    assert last.id == 3

    second_last = all_items[-2]
    assert second_last.id == 2


def test_paginated_list_limit(mock_client: MagicMock) -> None:
    """Test limit parameter to limit total results."""
    page1 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 11)],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(11, 21)],
        "paging": {"cursors": {"after": "cursor2"}},
    }

    page3 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(21, 31)],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2, page3]

    # Create paginated list with limit=15
    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"limit": 15, "page_size": 10},
    )

    # Fetch all items - should stop at 15
    items = list(paginated)

    assert len(items) == 15
    # Should have made only 2 requests (10 + 5 from second page)
    assert mock_client._request.call_count == 2


def test_paginated_list_limit_with_slicing(mock_client: MagicMock) -> None:
    """Test that slicing respects limit."""
    page1 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 11)],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(11, 21)],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2]

    # Create paginated list with limit=15
    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"limit": 15, "page_size": 10},
    )

    # Try to fetch 20, but should only get 15
    items = paginated[:20]

    assert len(items) == 15


def test_paginated_list_limit_with_iteration(mock_client: MagicMock) -> None:
    """Test that iteration respects limit."""
    page1 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 11)],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    page2 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(11, 21)],
        "paging": {"cursors": {"after": "cursor2"}},
    }

    page3 = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(21, 31)],
        "paging": {"cursors": {}},
    }

    mock_client._request.side_effect = [page1, page2, page3]

    # Create paginated list with limit=15
    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"limit": 15, "page_size": 10},
    )

    # Iterate and count items
    count = 0
    for item in paginated:
        count += 1

    assert count == 15
    # Should have made only 2 requests (stopped after getting 15 items)
    assert mock_client._request.call_count == 2


def test_paginated_list_page_size_larger_than_limit(mock_client: MagicMock) -> None:
    """Test that limit is respected even when page_size is larger.

    When page_size > limit, the API fetches page_size items but only
    limit items are returned to the user. This is slightly wasteful
    but the behavior is predictable: limit always takes precedence.
    """
    # API returns 20 items (page_size=20)
    mock_client._request.return_value = {
        "items": [{"id": i, "name": f"Item {i}"} for i in range(1, 21)],
        "paging": {"cursors": {"after": "cursor1"}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"limit": 5, "page_size": 20},
    )

    items = list(paginated)

    # Should only get 5 items despite page_size=20
    assert len(items) == 5
    assert items[0].id == 1
    assert items[4].id == 5

    # Should only make 1 request (got 20 items from API, only needed 5)
    assert mock_client._request.call_count == 1

    # Verify page_size was sent as "limit" to API
    mock_client._request.assert_called_once_with("GET", "/test", params={"limit": 20})


def test_paginated_list_page_size(mock_client: MagicMock) -> None:
    """Test that page_size is sent as 'limit' to the API."""
    mock_client._request.return_value = {
        "items": [{"id": 1, "name": "Item 1"}],
        "paging": {"cursors": {}},
    }

    paginated = PaginatedList(
        client=mock_client,
        endpoint="/test",
        model=MockModel,  # ty:ignore[invalid-argument-type]
        params={"page_size": 50},
    )

    # Fetch items
    list(paginated)

    # Verify page_size was sent as "limit" to API
    mock_client._request.assert_called_once_with("GET", "/test", params={"limit": 50})
