from uuid import UUID

from app.core.models.card import Card

from ..interfaces import CardNotFoundError, CardsRepositoryInterface


class CardMemoryRepository(CardsRepositoryInterface):
    def __init__(self) -> None:
        self.storage: dict[UUID, Card] = dict()

    async def add(self, card: Card):
        self.storage[card.id] = card

    async def get(self, id: UUID) -> Card:
        card = self.storage.get(id)
        if card is None:
            raise CardNotFoundError(message=f"id: {id} not found in memmory repo")

        return card

    async def get_next_due(self, deck_id: UUID) -> Card:
        cards = await self.get_by_deck_id(deck_id=deck_id)
        if len(cards) == 0:
            raise CardNotFoundError(message="can't find any cards in the deck")
        return sorted(cards, key=lambda c: c.due)[0]

    async def get_by_deck_id(self, deck_id: UUID) -> list[Card]:
        cards: list[Card] = []

        for _, card in self.storage.items():
            if card.deck_id == deck_id:
                cards.append(card)

        return cards

    async def delete(self, id: UUID) -> None:
        del self.storage[id]

    async def update(self, card: Card) -> None:
        self.storage[card.id] = card
