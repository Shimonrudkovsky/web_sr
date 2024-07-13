from abc import ABC, abstractmethod
from uuid import UUID

from fsrs.models import SchedulingInfo

from core.models.card import Card
from core.models.deck import Deck
from core.models.template import CardTemplate


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


class CardsRepositoryInterface(ABC):
    @abstractmethod
    def add(self, card: Card):
        pass

    @abstractmethod
    def get(self, id: UUID) -> Card:
        pass

    @abstractmethod
    def get_by_deck_id(self, deck_id: UUID) -> list[Card]:
        pass

    @abstractmethod
    def delete(self, id: UUID):
        pass

    @abstractmethod
    def update(self, card: Card):
        pass

    @abstractmethod
    def get_next_due(self, deck_id: UUID) -> Card:
        pass


class TemplateRepositoryInterface(ABC):
    @abstractmethod
    def add(self, template: CardTemplate):
        pass

    @abstractmethod
    def get(self, id: UUID) -> CardTemplate:
        pass

    @abstractmethod
    def get_all(self) -> list[UUID]:
        pass

    @abstractmethod
    def delete(self, id: UUID):
        pass


class DeckRepositoryInterface(ABC):
    @abstractmethod
    def add(self, deck: Deck) -> UUID:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Deck:
        pass

    @abstractmethod
    def get_all(self) -> list[Deck]:
        pass

    @abstractmethod
    def delete(self, id: UUID):
        pass


class ReviewLogRepositoryInterface(ABC):
    @abstractmethod
    def add(self, scheduled_card: SchedulingInfo):
        pass
