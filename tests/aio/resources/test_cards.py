from __future__ import annotations

import pytest

import clash_royale
from clash_royale.aio import Client
from clash_royale.aio.pagination import PaginatedList
from clash_royale.models.card import Card


@pytest.mark.vcr()
async def test_list_cards(client: Client) -> None:
    """Test listing cards with full model validation."""
    cards = client.cards.list(limit=10, page_size=10)

    assert isinstance(cards, PaginatedList)

    cards_list = await cards.all()
    assert len(cards_list) == 10

    for card in cards_list:
        assert isinstance(card, Card)
        assert card.name is not None
        assert card.id > 0
        assert card.max_level > 0

        assert card.icon_urls is not None
        assert card.icon_urls.medium is not None
        assert "http" in card.icon_urls.medium


@pytest.mark.vcr()
async def test_list_cards_no_params(client: Client) -> None:
    """Test listing cards without limit/page_size."""
    cards = client.cards.list()

    assert isinstance(cards, PaginatedList)

    first_cards = await cards.slice(0, 5)
    assert len(first_cards) == 5
    assert all(isinstance(card, Card) for card in first_cards)


async def test_cards_resource_initialization(client: Client) -> None:
    """Test Cards resource initialization."""
    assert client.cards is not None
    assert client.cards._client == client


@pytest.mark.vcr()
async def test_list_cards_unauthorized() -> None:
    """Test listing cards with invalid API key."""
    client = Client(api_key="invalid_key_12345")

    cards = client.cards.list()

    with pytest.raises(clash_royale.ClashRoyaleUnauthorizedError):
        await cards.all()

    await client.aclose()
