from uuid import UUID, uuid4

from core.models.template import CardTemplate
from ..interfaces import TemplateRepositoryInterface, TemplateNotFoundError

class TemplateMemmoryRepository(TemplateRepositoryInterface):
    def __init__(self):
        self.storage = dict()
    
    def add(self, template: CardTemplate):
        self.storage[template.id] = template
    
    def get(self, id: UUID) -> CardTemplate:
        template = self.storage.get(id)

        if not template:
            raise TemplateNotFoundError(message=f"id: {id} not found in memmory repo")
    
        return template
    
    def get_all(self) -> list[UUID]:
        return self.storage.keys()

    def delete(self, id: UUID):
        del(self.storage[id])

