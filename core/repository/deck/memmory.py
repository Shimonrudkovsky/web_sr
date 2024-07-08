from uuid import UUID

from ..interfaces import DeckRepositoryInterface, DeckNotFoundError
from core.models.deck import Deck

class DeckMemmoryRepository(DeckRepositoryInterface):
    def __init__(self) -> None:
        self.storage = dict()

    def add(self, deck: Deck) -> UUID:
        self.storage[deck.id] = deck
    
    def get(self, id: UUID) -> Deck:
        deck = self.storage.get(id)

        if not deck:
            raise DeckNotFoundError(message=f"id: {id} not found in memmory repo")
        
        return deck

    def get_all(self) -> list[Deck]:
        return self.storage.values()
    
    def delete(self, id: UUID):
        del(self.storage[id])
