from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from fsrs.models import SchedulingInfo

from app.core.models.card import Card
from app.core.models.deck import Deck
from app.core.models.template import CardTemplate


class GeneralError(Exception):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message


class RepositoryError(GeneralError):
    pass


class CardNotFoundError(RepositoryError):
    pass


class TemplateNotFoundError(RepositoryError):
    pass


class DeckNotFoundError(RepositoryError):
    pass


class AbstractRepository(ABC):
    storage: Any

    @abstractmethod
    def __init__(self, storage: Any) -> None:
        pass


class CardsRepositoryInterface(AbstractRepository):
    @abstractmethod
    async def add(self, card: Card) -> UUID:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Card:
        pass

    @abstractmethod
    async def get_by_deck_id(self, deck_id: UUID) -> list[Card]:
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        pass

    @abstractmethod
    async def update(self, card: Card):
        pass

    @abstractmethod
    async def get_next_due(self, deck_id: UUID) -> Card:
        pass


class TemplateRepositoryInterface(AbstractRepository):
    @abstractmethod
    async def add(self, template: CardTemplate):
        pass

    @abstractmethod
    async def get(self, id: UUID) -> CardTemplate:
        pass

    @abstractmethod
    async def get_all(self) -> list[CardTemplate]:
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        pass


class DeckRepositoryInterface(AbstractRepository):
    @abstractmethod
    async def add(self, deck: Deck) -> UUID:
        pass

    @abstractmethod
    async def get(self, id: UUID) -> Deck:
        pass

    @abstractmethod
    async def get_all(self) -> list[Deck]:
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        pass


class ReviewLogRepositoryInterface(AbstractRepository):
    @abstractmethod
    async def add(self, scheduling_info: SchedulingInfo):
        pass
