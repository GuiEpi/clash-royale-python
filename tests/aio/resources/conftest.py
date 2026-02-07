from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def vcr_cassette_dir():
    """Reuse cassettes from the sync resource tests."""
    return str(Path(__file__).parent.parent.parent / "resources" / "cassettes")
