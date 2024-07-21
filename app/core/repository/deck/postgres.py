from uuid import UUID

from app.core.models.deck import Deck
from app.db.postgres import AsyncPGStorage

from ..interfaces import DeckRepositoryInterface


class DeckPostgresRepository(DeckRepositoryInterface):
    def __init__(self, storage: AsyncPGStorage) -> None:
        self.storage = storage

    async def add(self, deck: Deck):
        query = """
        INSERT INTO web_sr.decks (id, name)
            VALUES (%s, %s);
        """
        await self.storage.execute(query=query, params=(deck.id, deck.name))

    async def get(self, id: UUID) -> Deck:
        query = """
        SELECT id, name FROM web_sr.decks
        WHERE id = %s;
        """
        result = await self.storage.fetch(query=query, params=(id,))

        return Deck(**result[0])

    async def get_all(self) -> list[Deck]:
        query = """
        SELECT id, name FROM web_sr.decks;
        """
        result = await self.storage.fetch(query=query)

        return [Deck(**i) for i in result]

    async def delete(self, id: UUID):
        query = """
        DELETE FROM web_sr.decks WHERE id = %s;
        """
        await self.storage.execute(query=query, params=(id,))
