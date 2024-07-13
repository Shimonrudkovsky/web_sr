from uuid import UUID

from core.models.template import CardTemplate

from ..interfaces import TemplateNotFoundError, TemplateRepositoryInterface


class TemplateMemmoryRepository(TemplateRepositoryInterface):
    def __init__(self) -> None:
        self.storage: dict[UUID, CardTemplate] = dict()

    def add(self, template: CardTemplate) -> None:
        self.storage[template.id] = template

    def get(self, id: UUID) -> CardTemplate:
        template = self.storage.get(id)

        if not template:
            raise TemplateNotFoundError(message=f"id: {id} not found in memmory repo")

        return template

    def get_all(self) -> list[UUID]:
        templates: list[UUID] = list(self.storage.keys())
        if templates == []:
            raise TemplateNotFoundError(message="template list is empty")

        return templates

    def delete(self, id: UUID) -> None:
        del self.storage[id]
