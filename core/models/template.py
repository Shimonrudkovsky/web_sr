from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CardTemplateConfig(BaseModel):
    front: str
    back: str


class CardTemplate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    config: CardTemplateConfig
