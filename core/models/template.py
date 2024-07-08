from uuid import UUID, uuid4

class CardTemplateConfig():
    front: str
    back: str

    def __init__(self, front: str, back: str) -> None:
        self.front = front
        self.back = back

class CardTemplate():
    id: UUID
    config: CardTemplateConfig

    def __init__(self, front: str, back: str) -> None:
        self.id = uuid4()
        self.config = CardTemplateConfig(front=front, back=back)
