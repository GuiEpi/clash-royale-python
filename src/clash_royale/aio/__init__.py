"""Async implementation of the Clash Royale API client."""

from __future__ import annotations

from .client import Client
from .pagination import PaginatedList
from .resources import (
    Cards,
    Clans,
    GlobalTournaments,
    Leaderboards,
    Locations,
    Players,
    Tournaments,
)

__all__ = [
    "Cards",
    "Clans",
    "Client",
    "GlobalTournaments",
    "Leaderboards",
    "Locations",
    "PaginatedList",
    "Players",
    "Tournaments",
]
