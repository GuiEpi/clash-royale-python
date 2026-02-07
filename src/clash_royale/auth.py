from __future__ import annotations

from collections.abc import AsyncGenerator, Generator

import httpx

from .exceptions import InvalidAPIKeyError


class CRAuth(httpx.Auth):
    """
    Clash Royale Auth for httpx.

    Attaches the API key to the Authorization header of each request.
    Supports both sync and async httpx clients.

    :params api_key: Your Clash Royale API key.
    :raises ValueError: If the API key is empty or None.
    """

    def __init__(self, api_key: str):
        if not api_key or (isinstance(api_key, str) and not api_key.strip()):
            raise InvalidAPIKeyError()
        self.api_key = api_key

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        """Sync auth flow for httpx.Client."""
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        yield request

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        """Async auth flow for httpx.AsyncClient."""
        request.headers["Authorization"] = f"Bearer {self.api_key}"
        yield request
