import uvicorn
from fsrs import (
    FSRS,
    State,
    Rating,
)
from config.config import Config, Repositories
from api.init import ServerGenerator
from api.routers.service import service_router
from api.routers.card import card_router
from api.routers.deck import deck_router
from api.routers.template import template_router
from uuid import uuid4
from core.models.card import Card
from core.repository.card.memmory import CardMemoryRepository
from core.repository.template.memmory import TemplateMemmoryRepository
from core.repository.deck.memmory import DeckMemmoryRepository
from core.service import CardService
from core.models.card import Card
from core.models.template import CardTemplate
from core.models.deck import Deck


def init_test_repos(repos: Repositories):
    template_front = """
        <h2>{{Word}}</h2>
        <hr>
        {{Examples}}
    """
    template_back = """
        <h2>{{Word}}</h2>
        <p><small>{{info}}</small></p>
        <hr>
        {{Examples_translated}}
        <hr>
        <h3>{{Translation}}</h3>
        <p></p>
    """

    fields1 = {
        "Word": "sich freuen auf",
        "info": "AKK",
        "Translation": "to look forward to, to be excited about",
        "Examples": "1. example\n2. another example",
        "Examples_translated": "1. translated example\n2. another translated example",
    }
    fields2 = {
        "Word": "abhängen vo",
        "info": "DAT",
        "Translation": "depend on",
        "Examples": "1. example2\n2. another example2",
        "Examples_translated": "1. translated example2\n2. another translated example2",
    }


    t = CardTemplate(front=template_front, back=template_back)
    repos.templates.add(t)
    d = Deck(name="Test deck")
    repos.decks.add(deck=d)
    repos.decks.add(deck=Deck(name="Another test deck"))
    c1 = Card(template_id=t.id, deck_id=d.id, fields=fields1)
    repos.cards.add(c1)
    c2 = Card(template_id=t.id, deck_id=d.id, fields=fields2)
    repos.cards.add(c2)

    print(f"template id: {t.id}\ndeck id: {d.id}")


card_repo = CardMemoryRepository()
template_repo = TemplateMemmoryRepository()
deck_repo = DeckMemmoryRepository()
repos = Repositories(cards=card_repo, templates=template_repo, decks=deck_repo)
config = Config(8080, [service_router, card_router, deck_router, template_router], repos)
generator = ServerGenerator(config=config)
app = generator.initWebServer()

# TODO: remove after testing
init_test_repos(repos)

uvicorn.run(app, port=config.port)
