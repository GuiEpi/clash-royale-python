from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

import clash_royale

load_dotenv()


@pytest.fixture(scope="module")
def vcr_config():
    """VCR configuration for Clash Royale API tests.

    This configures how VCR records and replays HTTP interactions.
    """
    return {
        # Record mode: 'once' = record if cassette doesn't exist, then replay
        "record_mode": "once",
        # Match requests on these criteria
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
        # Filter sensitive data from cassettes (don't save real API key)
        "filter_headers": [
            ("authorization", "DUMMY_API_KEY"),
        ],
        # Decode compressed responses for human-readable cassettes
        "decode_compressed_response": True,
    }


@pytest.fixture
def api_key() -> str:
    """Return API key from environment or dummy key for playback.

    When recording new cassettes, set CLASH_ROYALE_API_KEY environment variable.
    When playing back existing cassettes, any key works.
    """
    return os.getenv("CLASH_ROYALE_API_KEY", "dummy_api_key_for_vcr_playback")


@pytest.fixture
def client(api_key: str) -> clash_royale.Client:
    """Return a test client.

    This client will use VCR to record/replay HTTP interactions.
    Uses the RoyaleAPI proxy for easier testing.
    """
    return clash_royale.Client(api_key=api_key, proxy="https://proxy.royaleapi.dev")
