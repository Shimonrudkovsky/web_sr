import json
from uuid import UUID

from app.core.models.card import Card
from app.db.postgres import PostgresStorage

from ..interfaces import CardsRepositoryInterface

keys = (
    "id",
    "template_id",
    "deck_id",
    "fields",
    "due",
    "stability",
    "difficulty",
    "elapsed_days",
    "scheduled_days",
    "reps",
    "lapses",
    "state",
    "last_review",
)


class CardsPostgresRepository(CardsRepositoryInterface):
    def __init__(self, storage: PostgresStorage):
        self.storage = storage

    async def add(self, card: Card) -> UUID:
        query = f"""
        INSERT INTO web_sr.cards (
            {", ".join(keys)}
        )
        VALUES ({", ".join("%s" for _ in range(len(keys)))})
        RETURNING id
        """
        result = await self.storage.fetch(
            query=query,
            params=(
                card.id,
                card.template_id,
                card.deck_id,
                json.dumps(card.fields),
                card.due,
                card.stability,
                card.difficulty,
                card.elapsed_days,
                card.scheduled_days,
                card.reps,
                card.lapses,
                card.state,
                card.last_review,
            ),
        )

        return result[0].get("id")

    async def get(self, id: UUID) -> Card:
        query = f"""
        SELECT
            {", ".join(keys)}
        FROM web_sr.cards
        WHERE id = %s
        """
        result = await self.storage.fetch(query=query, params=(id,))

        return Card(**result[0])

    async def get_by_deck_id(self, deck_id: UUID) -> list[Card]:
        query = f"""
        SELECT
            {", ".join(keys)}
        FROM web_sr.cards
        WHERE deck_id = %s
        """
        result = await self.storage.fetch(query=query, params=(deck_id,))

        return [Card.from_dict(i) for i in result]

    async def delete(self, id: UUID):
        query = """
        DELETE FROM web_sr.cards WHERE id = %s
        """
        await self.storage.execute(query=query, params=(id,))

    async def update(self, card: Card):
        query = """
        UPDATE web_sr.cards SET
            template_id=%s,
            deck_id=%s,
            fields=%s,
            due=%s,
            stability=%s,
            difficulty=%s,
            elapsed_days=%s,
            scheduled_days=%s,
            reps=%s,
            lapses=%s,
            state=%s,
            last_review=%s
        WHERE id = %s
        """
        _keys = keys[1:] + (keys[0],)
        card_dict = card.to_dict()
        card_dict["fields"] = json.dumps(card_dict["fields"])
        await self.storage.execute(query=query, params=tuple([card_dict.get(i) for i in _keys]))

    async def get_next_due(self, deck_id: UUID) -> Card:
        query = f"""
        SELECT
            {", ".join(keys)}
        FROM web_sr.cards
        WHERE deck_id = %s
        ORDER BY due DESC;
        """
        result = await self.storage.fetch(query=query, params=(deck_id,))

        return Card(**result[0])
