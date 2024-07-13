from typing import Union
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class CardTemplateConfig(BaseModel):
    front: str
    back: str


class CardTemplate(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    config: CardTemplateConfig
