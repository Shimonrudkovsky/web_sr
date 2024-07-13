from uuid import UUID

import jinja2
from fastapi import Request
from fsrs.models import SchedulingInfo

from core.models.card import Card
from core.models.deck import Deck
from core.models.template import CardTemplate
from core.repository.interfaces import (
    CardNotFoundError,
    CardsRepositoryInterface,
    DeckNotFoundError,
    DeckRepositoryInterface,
    RepositoryError,
    ReviewLogRepositoryInterface,
    TemplateNotFoundError,
    TemplateRepositoryInterface,
)
from schemas.response import CardResponse, CardTemplateResponse


class CardService:
    card_repository: CardsRepositoryInterface
    template_repository: TemplateRepositoryInterface
    deck_repository: DeckRepositoryInterface
    review_log_repository: ReviewLogRepositoryInterface

    def __init__(self, request: Request):
        self.card_repository = request.app.config.repositories.cards
        self.template_repository = request.app.config.repositories.templates
        self.deck_repository = request.app.config.repositories.decks
        self.review_log_repository = request.app.config.repositories.review_logs

    def _render_card(self, card: Card) -> CardResponse:
        try:
            template = self.template_repository.get(card.template_id)
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

    def get_card(self, card_id: UUID) -> Card:
        try:
            return self.card_repository.get(card_id)
        except CardNotFoundError as err:
            raise err

    def get_next_due(self, deck_id: UUID) -> CardResponse:
        try:
            card = self.card_repository.get_next_due(deck_id=deck_id)
        except CardNotFoundError as err:
            raise err

        card_resp = self._render_card(card=card)

        return card_resp

    def get_card_response(self, card_id: UUID) -> CardResponse:
        try:
            card = self.card_repository.get(card_id)
        except CardNotFoundError as err:
            raise err

        card_resp = self._render_card(card=card)

        return card_resp

    def new_card(
        self,
        template_id: UUID,
        deck_id: UUID,
        fields: dict,
    ) -> UUID:
        card = Card(template_id=template_id, deck_id=deck_id, fields=fields)
        try:
            self.card_repository.add(card)
        except RepositoryError as err:
            raise err

        return card.id

    def add_template(self, template: CardTemplate):
        try:
            self.template_repository.add(template)
        except RepositoryError as err:
            raise err

    def update(self, scheduled_card: SchedulingInfo):
        self.card_repository.update(card=scheduled_card.card)
        self.review_log_repository.add(scheduled_card=scheduled_card)


class DeckService:
    deck_repository: DeckRepositoryInterface
    card_repository: CardsRepositoryInterface

    def __init__(self, request: Request) -> None:
        self.deck_repository: DeckRepositoryInterface = request.app.config.repositories.decks
        self.card_repository: CardsRepositoryInterface = request.app.config.repositories.cards

    def new_deck(self, name: str) -> UUID:
        deck = Deck(name=name)
        self.deck_repository.add(deck)
        return deck.id

    def get_deck_info(self, deck_id: UUID) -> list[UUID]:
        try:
            cards: list[Card] = self.card_repository.get_by_deck_id(deck_id=deck_id)
            return [c.id for c in cards]
        except DeckNotFoundError as err:
            raise err

    def decks_list(self) -> list[Deck]:
        try:
            decs = self.deck_repository.get_all()
        except RepositoryError as err:
            raise err

        if decs == []:
            raise DeckNotFoundError(message="deck list is empty")

        return decs

    def delete(self, deck_id: UUID):
        self.deck_repository.delete(deck_id)


class TemplateService:
    template_repository: TemplateRepositoryInterface

    def __init__(self, request: Request):
        self.template_repository = request.app.config.repositories.templates

    def template_list(self) -> list[UUID]:
        return self.template_repository.get_all()
