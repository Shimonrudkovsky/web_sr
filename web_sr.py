import uvicorn

from fastapi import FastAPI


from app.api.init import ServerGenerator
from app.api.routers.card import card_router
from app.api.routers.deck import deck_router
from app.api.routers.service import service_router
from app.api.routers.template import template_router
from app.config.config import Config, Repositories
from app.core.models.card import Card
from app.core.models.deck import Deck
from app.core.models.template import CardTemplate, CardTemplateConfig
from app.core.repository.card.memmory import CardMemoryRepository
from app.core.repository.deck.memmory import DeckMemmoryRepository
from app.core.repository.review_log.memmory import ReviewLogMemmoryRepository
from app.core.repository.template.memmory import TemplateMemmoryRepository
from app.exceptions.handlers import add_exeption_handlers


def init_repos_with_test_data(repos: Repositories):
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


def init_repositories() -> Repositories:
    card_repo = CardMemoryRepository()
    template_repo = TemplateMemmoryRepository()
    deck_repo = DeckMemmoryRepository()
    review_log = ReviewLogMemmoryRepository()

    return Repositories(cards=card_repo, templates=template_repo, decks=deck_repo, review_logs=review_log)


def init_config(repositories: Repositories) -> Config:
    return Config(8080, [service_router, card_router, deck_router, template_router], repositories)


def init_app(config: Config) -> FastAPI:
    generator = ServerGenerator(config=config)
    app = generator.initWebServer()

    add_exeption_handlers(app=app)

    return app


repos = init_repositories()
config = init_config(repositories=repos)

# TODO: remove after testing
init_repos_with_test_data(repos)

if __name__ == "__main__":
    app = init_app(config)
    uvicorn.run(app, port=config.port)
else:
    app = init_app(config)
