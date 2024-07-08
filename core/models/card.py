from uuid import UUID, uuid4
from fsrs import Card as OriginalCard


class Card(OriginalCard):
    id: UUID
    template_id: UUID
    deck_id: UUID
    fields: dict

    def __init__(self, template_id: UUID, deck_id: UUID, fields: dict, *args, **kwargs):
        self.id = uuid4()
        self.template_id = template_id
        self.deck_id = deck_id
        self.fields = fields
        super().__init__(*args, **kwargs)
    
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
        }

        if hasattr(self, "last_review"):
            return_dict["last_review"] = self.last_review.isoformat()

        return return_dict
