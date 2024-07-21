from uuid import UUID

from app.core.models.template import CardTemplate, CardTemplateConfig
from app.core.repository.interfaces import TemplateRepositoryInterface
from app.db.postgres import AsyncPGStorage


class TemplatePostgresReposytory(TemplateRepositoryInterface):
    def __init__(self, storage: AsyncPGStorage):
        self.storage = storage

    async def add(self, template: CardTemplate):
        query = """
        INSERT INTO web_sr.templates (id, config) VALUES (%s, %s)
        """
        await self.storage.execute(query=query, params=(template.id, template.config.model_dump_json()))

    async def get(self, id: UUID) -> CardTemplate:
        query = """
        SELECT id, config FROM web_sr.templates WHERE id = %s
        """
        result = await self.storage.fetch(query=query, params=(id,))

        return CardTemplate(**result[0])

    async def get_all(self) -> list[CardTemplate]:
        query = """
        SELECT id, config FROM web_sr.templates;
        """
        result = await self.storage.fetch(query=query)

        return [CardTemplate(id=i["id"], config=CardTemplateConfig(**i.get("config"))) for i in result]

    async def delete(self, id: UUID):
        query = """
        DELETE FROM web_sr.templates WHERE id = %s;
        """
        await self.storage.execute(query=query, params=(id,))
