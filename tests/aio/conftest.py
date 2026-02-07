from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from clash_royale.aio import Client

load_dotenv()


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for async Clash Royale API tests."""
    return {
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        "filter_headers": [
            ("authorization", "DUMMY_API_KEY"),
        ],
        "decode_compressed_response": True,
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    """Reuse cassettes from the sync client tests."""
    return str(Path(__file__).parent.parent / "cassettes")


@pytest.fixture
def api_key() -> str:
    """Return API key from environment or dummy key for playback."""
    return os.getenv("CLASH_ROYALE_API_KEY", "dummy_api_key_for_vcr_playback")


@pytest_asyncio.fixture
async def client(api_key: str) -> AsyncGenerator[Client, None]:
    """Return an async test client.

    Uses the RoyaleAPI proxy for easier testing.
    """
    client = Client(api_key=api_key, proxy="https://proxy.royaleapi.dev")
    yield client
    await client.aclose()
