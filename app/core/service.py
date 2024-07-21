from uuid import UUID

import jinja2
from fastapi import Depends
from fsrs.models import SchedulingInfo

from app.core.models.card import Card
from app.core.models.deck import Deck
from app.core.models.template import CardTemplate
from app.core.repository import Repositories, get_repositories
from app.core.repository.interfaces import (
    CardNotFoundError,
    CardsRepositoryInterface,
    DeckNotFoundError,
    DeckRepositoryInterface,
    RepositoryError,
    ReviewLogRepositoryInterface,
    TemplateNotFoundError,
    TemplateRepositoryInterface,
)
from app.schemas.response import CardResponse, CardTemplateResponse


class CardService:
    card_repository: CardsRepositoryInterface
    template_repository: TemplateRepositoryInterface
    deck_repository: DeckRepositoryInterface
    review_log_repository: ReviewLogRepositoryInterface

    def __init__(self, repositories: Repositories = Depends(get_repositories)):
        self.card_repository = repositories.cards
        self.template_repository = repositories.templates
        self.deck_repository = repositories.decks
        self.review_log_repository = repositories.review_logs

    async def _render_card(self, card: Card) -> CardResponse:
        try:
            template = await self.template_repository.get(card.template_id)
        except TemplateNotFoundError as err:
            raise err

        front = jinja2.Template(template.config.front)
        back = jinja2.Template(template.config.back)
        card_resp = CardResponse(
            id=card.id,
            deck_id=card.deck_id,
            fields=card.fields,
            due=card.due,
            template=CardTemplateResponse(front=front.render(card.fields), back=back.render(card.fields)),
        )

        return card_resp

    async def get_card(self, card_id: UUID) -> Card:
        try:
            card = await self.card_repository.get(card_id)
            card.localize_timestamps()
            return card
        except CardNotFoundError as err:
            raise err

    async def get_next_due(self, deck_id: UUID) -> CardResponse:
        try:
            card = await self.card_repository.get_next_due(deck_id=deck_id)
        except CardNotFoundError as err:
            raise err

        card_resp = await self._render_card(card=card)

        return card_resp

    async def get_card_response(self, card_id: UUID) -> CardResponse:
        try:
            card = await self.card_repository.get(card_id)
        except CardNotFoundError as err:
            raise err

        card_resp = await self._render_card(card=card)

        return card_resp

    async def new_card(
        self,
        template_id: UUID,
        deck_id: UUID,
        fields: dict,
    ) -> UUID:
        id = None
        card = Card(template_id=template_id, deck_id=deck_id, fields=fields)
        try:
            id = await self.card_repository.add(card)
        except RepositoryError as err:
            raise err

        return id

    async def add_template(self, template: CardTemplate):
        try:
            await self.template_repository.add(template)
        except RepositoryError as err:
            raise err

    async def update(self, scheduled_card: SchedulingInfo):
        await self.card_repository.update(card=scheduled_card.card)
        await self.review_log_repository.add(scheduling_info=scheduled_card)


class DeckService:
    deck_repository: DeckRepositoryInterface
    card_repository: CardsRepositoryInterface

    def __init__(self, repositories: Repositories = Depends(get_repositories)) -> None:
        self.deck_repository: DeckRepositoryInterface = repositories.decks
        self.card_repository: CardsRepositoryInterface = repositories.cards

    async def new_deck(self, name: str) -> UUID:
        deck = Deck(name=name)
        await self.deck_repository.add(deck)
        return deck.id

    async def get_deck_info(self, deck_id: UUID) -> list[UUID]:
        try:
            cards: list[Card] = await self.card_repository.get_by_deck_id(deck_id=deck_id)
            return [c.id for c in cards]
        except DeckNotFoundError as err:
            raise err

    async def decks_list(self) -> list[Deck]:
        try:
            decs = await self.deck_repository.get_all()
        except RepositoryError as err:
            raise err

        if decs == []:
            raise DeckNotFoundError(message="deck list is empty")

        return decs

    async def delete(self, deck_id: UUID):
        await self.deck_repository.delete(deck_id)


class TemplateService:
    template_repository: TemplateRepositoryInterface

    def __init__(self, repositories: Repositories = Depends(get_repositories)):
        self.template_repository = repositories.templates

    async def template_list(self) -> list[UUID]:
        result = await self.template_repository.get_all()

        return [i.id for i in result]
