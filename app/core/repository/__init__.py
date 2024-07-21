from fastapi import Request

from app.core.repository.card.postgres import CardsPostgresRepository
from app.core.repository.interfaces import (
    CardsRepositoryInterface,
    DeckRepositoryInterface,
    ReviewLogRepositoryInterface,
    TemplateRepositoryInterface,
)
from app.db.postgres import AsyncPGStorage

from .deck.postgres import DeckPostgresRepository
from .review_log.postgres import ReviewLogPostgresRepository
from .template.postgres import TemplatePostgresReposytory


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


async def get_repositories(request: Request) -> Repositories:
    storage = await AsyncPGStorage.init(request.app.config.db)
    card_repo = CardsPostgresRepository(storage=storage)
    template_repo = TemplatePostgresReposytory(storage=storage)
    deck_repo = DeckPostgresRepository(storage=storage)
    # review_log = ReviewLogMemmoryRepository()
    review_log = ReviewLogPostgresRepository(storage=storage)

    return Repositories(cards=card_repo, templates=template_repo, decks=deck_repo, review_logs=review_log)
