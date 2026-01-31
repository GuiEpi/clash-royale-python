from __future__ import annotations

import pytest

import clash_royale
from clash_royale.models.card import Card
from clash_royale.pagination import PaginatedList


@pytest.mark.vcr()
def test_list_cards(client: clash_royale.Client) -> None:
    """Test listing cards with full model validation.

    This test covers:
    - Basic API call and PaginatedList behavior
    - Limit/page_size parameters
    - Card model fields including icon URLs
    """
    cards = client.cards.list(limit=10, page_size=10)

    assert isinstance(cards, PaginatedList)

    cards_list = list(cards)
    assert len(cards_list) == 10

    # Validate all cards
    for card in cards_list:
        assert isinstance(card, Card)
        assert card.name is not None
        assert card.id > 0
        assert card.max_level > 0

        # Icon URLs should be present
        assert card.icon_urls is not None
        assert card.icon_urls.medium is not None
        assert "http" in card.icon_urls.medium


@pytest.mark.vcr()
def test_list_cards_no_params(client: clash_royale.Client) -> None:
    """Test listing cards without limit/page_size.

    Uses API defaults - fetches first batch of cards.
    """
    cards = client.cards.list()

    assert isinstance(cards, PaginatedList)

    # Just fetch first few to avoid fetching all cards
    first_cards = cards[:5]
    assert len(first_cards) == 5
    assert all(isinstance(card, Card) for card in first_cards)


def test_cards_resource_initialization(client: clash_royale.Client) -> None:
    """Test Cards resource initialization."""
    assert client.cards is not None
    assert client.cards._client == client


@pytest.mark.vcr()
def test_list_cards_unauthorized() -> None:
    """Test listing cards with invalid API key."""
    client = clash_royale.Client(api_key="invalid_key_12345")

    cards = client.cards.list()

    # PaginatedList will raise error when trying to fetch
    with pytest.raises(clash_royale.ClashRoyaleUnauthorizedError):
        list(cards)
