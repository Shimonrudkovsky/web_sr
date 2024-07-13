import uvicorn

from api.init import ServerGenerator
from api.routers.card import card_router
from api.routers.deck import deck_router
from api.routers.service import service_router
from api.routers.template import template_router
from config.config import Config, Repositories
from core.models.card import Card
from core.models.deck import Deck
from core.models.template import CardTemplate, CardTemplateConfig
from core.repository.card.memmory import CardMemoryRepository
from core.repository.deck.memmory import DeckMemmoryRepository
from core.repository.review_log.memmory import ReviewLogMemmoryRepository
from core.repository.template.memmory import TemplateMemmoryRepository
from exceptions.handlers import add_exeption_handlers


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

    t = CardTemplate(config=CardTemplateConfig(front=template_front, back=template_back))
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
review_log = ReviewLogMemmoryRepository()
repos = Repositories(cards=card_repo, templates=template_repo, decks=deck_repo, review_logs=review_log)
config = Config(8080, [service_router, card_router, deck_router, template_router], repos)
generator = ServerGenerator(config=config)
app = generator.initWebServer()

add_exeption_handlers(app=app)

# TODO: remove after testing
init_test_repos(repos)

uvicorn.run(app, port=config.port)
