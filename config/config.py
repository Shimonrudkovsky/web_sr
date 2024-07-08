from pydantic import BaseModel
from fastapi import APIRouter
from core.repository.interfaces import (
    CardsRepositoryInterface,
    TemplateRepositoryInterface,
    DeckRepositoryInterface,
)

class ConfigError(Exception):
    def __init__(self, message):
        self.message = "Config error: " + message
        super().__init__(self.message)


class Repositories():
    cards: CardsRepositoryInterface
    templates: TemplateRepositoryInterface
    decks: DeckRepositoryInterface

    def __init__(
        self,
        cards: CardsRepositoryInterface,
        templates: TemplateRepositoryInterface,
        decks: DeckRepositoryInterface
    ):
        self.cards = cards
        self.templates = templates
        self.decks = decks


class Config():
    port: int
    routers: list[APIRouter]
    repositories: Repositories

    def __init__(
            self,
            port: int,
            routers: list[APIRouter] = None,
            repositories: Repositories = None,
        ) -> None:
        if port is None:
            raise ConfigError("port is None")
        self.port = port
        if not routers or routers == []:
            raise ConfigError("no routers found")
        self.routers = routers if routers else []
        if not repositories:
            raise ConfigError("no repositories found")
        self.repositories = repositories
