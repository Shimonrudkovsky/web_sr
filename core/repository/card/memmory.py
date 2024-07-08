from uuid import UUID

from ..interfaces import CardsRepositoryInterface, CardNotFoundError
from core.models.card import Card


class CardMemoryRepository(CardsRepositoryInterface):
    def __init__(self):
        self.storage: dict[UUID, Card] = dict()

    def add(self, card: Card):
        self.storage[card.id] = card
    
    def get(self, id: UUID) -> Card:
        card = self.storage.get(id)
        if card is None:
            raise CardNotFoundError(f"id: {id} not found in memmory repo")

        return card

    def get_by_deck_id(self, deck_id: UUID) -> list[UUID]:
        card_ids: list[UUID] = []

        for _, card in self.storage.items():
            if card.deck_id == deck_id:
                card_ids.append(card.id)
        
        return card_ids

    def delete(self, id: UUID):
        del(self.storage[id])

    def update(self, card: Card):
        self.storage[card.id] = card
