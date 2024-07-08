from abc import ABC, abstractmethod

from uuid import UUID

from core.models.card import Card
from core.models.template import CardTemplate
from core.models.deck import Deck


class GeneralError(Exception):
    message: str

class RepositoryError(GeneralError):
    def __init__(self, message: str) -> None:
        self.message = message
    
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
    def get_by_deck_id(self, deck_id: UUID) -> list[UUID]:
        pass

    @abstractmethod
    def delete(self, id: UUID):
        pass

    @abstractmethod
    def update(self, card: Card):
        pass


class TemplateRepositoryInterface(ABC):
    @abstractmethod
    def add(self, template: CardTemplate):
        pass

    @abstractmethod
    def get(self, id: UUID) -> CardTemplate:
        pass

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