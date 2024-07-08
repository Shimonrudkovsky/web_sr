from uuid import UUID
from pydantic import BaseModel

class CardTemplate(BaseModel):
    front: str
    back: str

class CardResponse(BaseModel):
    id: UUID
    fields: dict
    template: CardTemplate

class DeckResponse(BaseModel):
    id: UUID
    name: str
