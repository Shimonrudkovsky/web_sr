from typing import TypeVar, Union
from uuid import UUID, uuid4

import pytz
from fsrs import Card as OriginalCard

CardType = TypeVar("CardType", bound="Card")


class Card(OriginalCard):
    id: UUID
    template_id: UUID
    deck_id: UUID
    fields: dict

    def __init__(self, template_id: UUID, deck_id: UUID, fields: dict, *args, id: Union[UUID, None] = None, **kwargs):
        self.id = id if id else uuid4()
        self.template_id = template_id
        self.deck_id = deck_id
        self.fields = fields
        super().__init__(*args, **kwargs)
        self.last_review = kwargs.get("last_review")

    def to_dict(self):
        return_dict = {
            "id": self.id,
            "deck_id": self.deck_id,
            "template_id": self.template_id,
            "due": self.due.isoformat() if self.due else None,
            "stability": self.stability,
            "difficulty": self.difficulty,
            "elapsed_days": self.elapsed_days,
            "scheduled_days": self.scheduled_days,
            "reps": self.reps,
            "lapses": self.lapses,
            "state": self.state,
            "fields": self.fields,
            "last_review": self.last_review.isoformat() if hasattr(self, "last_review") else None,
        }

        return return_dict

    @classmethod
    def from_dict(cls, d: dict) -> CardType:
        return Card(**d)

    def localize_timestamps(self):
        if self.last_review:
            self.last_review = pytz.utc.localize(self.last_review)
        self.due = pytz.utc.localize(self.due)
