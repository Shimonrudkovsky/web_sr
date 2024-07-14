import os
import sys
from uuid import UUID

import pytest

from app.config.config import Repositories
from app.core.models.card import Card
from app.core.models.deck import Deck
from app.core.models.template import CardTemplate
from app.core.repository.interfaces import (
    CardsRepositoryInterface,
    DeckRepositoryInterface,
    TemplateRepositoryInterface,
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def fake_repositories() -> Repositories:
    template_front = """
        <h2>{{Word}}</h2>
    """
    template_back = """
        <h2>{{Translation}}</h2>
    """

    deck = Deck(name="test deck")
    template = CardTemplate(front=template_front, back=template_back)

    card = Card(
        template_id=template.id,
        deck_id=deck.id,
        fields={"Word": "test word", "Translation": "test translation"},
    )

    class FakeCardsRepository(CardsRepositoryInterface):
        def add(self, card: Card):
            return

        def get(self, id: UUID) -> Card:
            return card

        def delete(self, id: UUID):
            return

        def update(self, card: Card):
            return

    class FakeTemplateRepository(TemplateRepositoryInterface):
        def add(self, template: CardTemplate):
            pass

        def delete(self, id: UUID):
            pass

        def get(self, id: UUID) -> CardTemplate:
            return template

    class FakeDeckRepository(DeckRepositoryInterface):
        def add(self, deck: Deck):
            pass

        def delete(self, id: UUID):
            pass

        def get(self, id: UUID) -> Deck:
            return

        def get_all(self) -> list[Deck]:
            return [deck, Deck(name="test deck2")]

    FakeCardsRepository()
    template_repo = FakeTemplateRepository()
    deck_repo = FakeDeckRepository()
    return Repositories(cards=FakeCardsRepository(), templates=template_repo, decks=deck_repo)
