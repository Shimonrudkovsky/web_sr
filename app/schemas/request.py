from uuid import UUID

from pydantic import BaseModel


class NewDeckRequest(BaseModel):
    name: str


class RateCardRequest(BaseModel):
    rating: int


class NewCardrequest(BaseModel):
    template_id: UUID
    deck_id: UUID
    fields: dict[str, str]
