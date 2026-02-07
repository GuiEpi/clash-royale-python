from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Generic, TypeVar

from ..models.base import CRBaseModel
from ..types import ClanSearchParams, PaginationParams

if TYPE_CHECKING:
    from .client import Client

ResourceType = TypeVar("ResourceType", bound="CRBaseModel")


class PaginatedList(Generic[ResourceType]):
    """Async lazy-loading paginated list that fetches pages on demand.

    Supports async iteration and explicit async methods for indexed access.

    Example usage::

        # Async iteration (lazy loading)
        async for clan in client.clans.search("royal"):
            print(clan.name)

        # Explicit index access
        clan = await results.get(5)

        # Explicit slice access
        clans = await results.slice(0, 10)

        # Fetch all results
        all_clans = await results.all()
    """

    def __init__(
        self,
        client: Client,
        endpoint: str,
        model: type[ResourceType],
        params: PaginationParams | ClanSearchParams | None = None,
    ):
        self._client = client
        self._endpoint = endpoint
        self._model = model

        # Extract client-side pagination control params
        _params = params.copy() if params else {}
        self._limit: int | None = _params.pop("limit", None)
        self._page_size: int | None = _params.pop("page_size", None)

        # Remaining params are for the API (after, before, etc.)
        self._params: dict[str, str | int] = _params

        self._elements: list[ResourceType] = []
        self._after_cursor: str | None = None
        self._has_more: bool = True

    def __repr__(self) -> str:
        loaded = len(self._elements)
        status = "more available" if self._has_more else "complete"
        return f"<{self.__class__.__name__} [{loaded} loaded, {status}]>"

    async def __aiter__(self) -> AsyncGenerator[ResourceType, None]:
        """Async iterate over all items, fetching pages as needed."""
        for item in self._elements:
            yield item

        while self._has_more and (
            self._limit is None or len(self._elements) < self._limit
        ):
            new_items = await self._grow()
            for item in new_items:
                yield item

    async def get(self, index: int) -> ResourceType:
        """Get item at index, fetching pages as needed.

        :param index: The index of the item to retrieve.
        :returns: The item at the specified index.
        :raises IndexError: If index is out of range.
        :raises ValueError: If index is negative.
        """
        if index < 0:
            raise ValueError(
                "Negative indexing is not supported because it requires "
                "fetching all pages. Use `await results.all()` and index "
                "the resulting list instead."
            )
        await self._fetch_to_index(index)
        return self._elements[index]

    async def slice(self, start: int, stop: int) -> list[ResourceType]:
        """Get a slice of items, fetching pages as needed.

        :param start: Start index (inclusive).
        :param stop: Stop index (exclusive).
        :returns: List of items in the specified range.
        """
        await self._fetch_to_index(stop - 1)
        return self._elements[start:stop]

    async def all(self) -> list[ResourceType]:
        """Fetch and return all items.

        .. warning:: This method fetches all pages from the API, which may
            result in many requests and large memory usage for endpoints
            with many results. Consider using ``limit`` or async iteration
            for large datasets.

        :returns: List of all items.
        """
        await self._fetch_all()
        return list(self._elements)

    async def first(self) -> ResourceType | None:
        """Get the first item, or None if empty.

        :returns: The first item or None.
        """
        try:
            return await self.get(0)
        except IndexError:
            return None

    def _could_grow(self) -> bool:
        """Check if more items can be fetched."""
        if self._limit is not None and len(self._elements) >= self._limit:
            return False
        return self._has_more

    async def _grow(self) -> list[ResourceType]:
        """Fetch the next page and add items to the list."""
        new_elements = await self._fetch_next_page()
        # If limit is set, only add elements up to the limit
        if self._limit is not None:
            remaining = self._limit - len(self._elements)
            if remaining <= 0:
                return []
            new_elements = new_elements[:remaining]
        self._elements.extend(new_elements)
        return new_elements

    async def _fetch_next_page(self) -> list[ResourceType]:
        """Fetch the next page from the API."""
        params = self._params.copy()

        if self._after_cursor:
            params["after"] = self._after_cursor

        if self._page_size:
            # Send page_size as "limit" to the API
            params["limit"] = self._page_size

        response = await self._client._request("GET", self._endpoint, params=params)

        # Update cursor for next page
        paging = response.get("paging", {})
        cursors = paging.get("cursors", {})
        self._after_cursor = cursors.get("after")
        self._has_more = self._after_cursor is not None

        # Parse items with model
        items = response.get("items", [])
        return [self._model.model_validate(item) for item in items]

    async def _fetch_to_index(self, index: int) -> None:
        """Fetch pages until the specified index is available."""
        while len(self._elements) <= index and self._could_grow():
            await self._grow()

    async def _fetch_all(self) -> None:
        """Fetch all remaining pages."""
        while self._could_grow():
            await self._grow()
