from uuid import UUID

from app.core.models.deck import Deck

from ..interfaces import DeckNotFoundError, DeckRepositoryInterface


class DeckMemmoryRepository(DeckRepositoryInterface):
    def __init__(self) -> None:
        self.storage: dict[UUID, Deck] = dict()

    def add(self, deck: Deck) -> UUID:
        self.storage[deck.id] = deck

        return deck.id

    def get(self, id: UUID) -> Deck:
        deck = self.storage.get(id)

        if not deck:
            raise DeckNotFoundError(message=f"id: {id} not found in memmory repo")

        return deck

    def get_all(self) -> list[Deck]:
        decks: list[Deck] = list(self.storage.values())
        if decks == []:
            raise DeckNotFoundError(message="empty deck list")

        return decks

    def delete(self, id: UUID) -> None:
        del self.storage[id]
