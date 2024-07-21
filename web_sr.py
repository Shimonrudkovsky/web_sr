from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.init import ServerGenerator
from app.api.routers.card import card_router
from app.api.routers.deck import deck_router
from app.api.routers.service import service_router
from app.api.routers.template import template_router
from app.config.config import Config, DBConfig, Lifespan
from app.core.models.card import Card
from app.core.models.deck import Deck
from app.core.models.template import CardTemplate, CardTemplateConfig
from app.core.repository import Repositories
from app.core.repository.card.postgres import CardsPostgresRepository
from app.core.repository.deck.postgres import DeckPostgresRepository
from app.core.repository.review_log.memmory import ReviewLogMemmoryRepository
from app.core.repository.template.postgres import TemplatePostgresReposytory
from app.db.postgres import AsyncPGStorage, PostgresStorage
from app.exceptions.handlers import add_exeption_handlers


async def init_repos_with_test_data(app: FastAPI):
    storage: PostgresStorage = await AsyncPGStorage.init(app.config.db)
    # card_repo = CardMemoryRepository()
    card_repo = CardsPostgresRepository(storage=storage)
    # template_repo = TemplateMemmoryRepository()
    template_repo = TemplatePostgresReposytory(storage=storage)
    deck_repo = DeckPostgresRepository(storage=storage)
    review_log = ReviewLogMemmoryRepository()

    repos = Repositories(cards=card_repo, templates=template_repo, decks=deck_repo, review_logs=review_log)

    async with repos.decks.storage.conn.cursor() as cur:
        await cur.execute("TRUNCATE web_sr.decks CASCADE;")
    async with repos.templates.storage.conn.cursor() as cur:
        await cur.execute("TRUNCATE web_sr.templates CASCADE;")

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
    await repos.templates.add(t)
    d = Deck(name="Test deck")
    await repos.decks.add(deck=d)
    await repos.decks.add(deck=Deck(name="Another test deck"))
    c1 = Card(template_id=t.id, deck_id=d.id, fields=fields1)
    await repos.cards.add(c1)
    c2 = Card(template_id=t.id, deck_id=d.id, fields=fields2)
    await repos.cards.add(c2)

    print(f"template id: {t.id}\ndeck id: {d.id}")


# async def init_repositories(db_config: DBConfig) -> Repositories:
#     conn = await AsyncPGStorage.init(db_config)
#     # card_repo = CardMemoryRepository()
#     card_repo = DeckPostgresRepository(conn=conn)
#     template_repo = TemplateMemmoryRepository()
#     deck_repo = DeckMemmoryRepository()
#     review_log = ReviewLogMemmoryRepository()

#     return Repositories(cards=card_repo, templates=template_repo, decks=deck_repo, review_logs=review_log)


def init_config(lifespan: Lifespan) -> Config:
    # TODO: remove hardcode
    db_config = DBConfig(
        host="localhost",
        database="postgres",
        user="postgres",
        password="",
    )
    return Config(
        port=8081,
        routers=[service_router, card_router, deck_router, template_router],
        lifespan=lifespan,
        db_cofig=db_config,
    )


def init_app(config: Config) -> FastAPI:
    generator = ServerGenerator(config=config)
    app = generator.initWebServer()

    add_exeption_handlers(app=app)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_repos_with_test_data(app)
    yield


config = init_config(lifespan=lifespan)

app = init_app(config)

if __name__ == "__main__":
    uvicorn.run(app, port=config.port)
