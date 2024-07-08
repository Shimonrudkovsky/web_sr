from uuid import UUID, uuid4

class Deck():
    id: UUID
    name: str

    def __init__(self, name: str) -> None:
        self.id = uuid4()
        self.name = name
