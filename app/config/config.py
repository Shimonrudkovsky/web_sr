from typing import Union

from fastapi import APIRouter
from fsrs import FSRS

from app.core.repository.interfaces import (
    CardsRepositoryInterface,
    DeckRepositoryInterface,
    ReviewLogRepositoryInterface,
    TemplateRepositoryInterface,
)


class ConfigError(Exception):
    def __init__(self, message):
        self.message = "Config error: " + message
        super().__init__(self.message)


class Repositories:
    cards: CardsRepositoryInterface
    templates: TemplateRepositoryInterface
    decks: DeckRepositoryInterface
    review_logs: ReviewLogRepositoryInterface

    def __init__(
        self,
        cards: CardsRepositoryInterface,
        templates: TemplateRepositoryInterface,
        decks: DeckRepositoryInterface,
        review_logs: ReviewLogRepositoryInterface,
    ):
        self.cards = cards
        self.templates = templates
        self.decks = decks
        self.review_logs = review_logs


class Config:
    port: int
    routers: list[APIRouter]
    repositories: Repositories
    fsrs: FSRS

    def __init__(
        self,
        port: int,
        routers: Union[list[APIRouter], None] = None,
        repositories: Union[Repositories, None] = None,
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
        self.fsrs = FSRS()
