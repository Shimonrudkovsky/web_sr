from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseExeptionResponse(BaseModel):
    message: str


class CardTemplateResponse(BaseModel):
    front: str
    back: str


class CardResponse(BaseModel):
    id: UUID
    deck_id: UUID
    template: CardTemplateResponse
    due: datetime


class DeckResponse(BaseModel):
    id: UUID
    name: str
