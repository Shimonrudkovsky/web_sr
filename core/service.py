from fastapi import Request
from uuid import UUID
from core.repository.interfaces import (
    CardsRepositoryInterface,
    CardNotFoundError,
    RepositoryError,
    TemplateRepositoryInterface,
    TemplateNotFoundError,
    DeckRepositoryInterface,
    DeckNotFoundError,
)

from core.models.card import Card
from core.models.template import CardTemplate
from core.models.deck import Deck
from schemas.response import CardResponse, CardTemplate
import jinja2


class CardService():
    card_repository: CardsRepositoryInterface
    template_repository: TemplateRepositoryInterface
    deck_repository: DeckRepositoryInterface

    def __init__(self, request: Request):
        self.card_repository = request.app.config.repositories.cards
        self.template_repository = request.app.config.repositories.templates
        self.deck_repository = request.app.config.repositories.decks

    def get_card_response(self, card_id: UUID) -> CardResponse:
        try:
            card = self.card_repository.get(card_id)
        except CardNotFoundError as err:
            raise err
        
        try:
            template = self.template_repository.get(card.template_id)
        except TemplateNotFoundError as err:
            raise err

        front = jinja2.Template(template.config.front)
        back = jinja2.Template(template.config.back)
        card_resp = CardResponse(
            id=card.id,
            fields=card.fields,
            template=CardTemplate(front=front.render(card.fields), back=back.render(card.fields)),
        )

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
        except RecursionError as err:
            raise err


class DeckService():
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
            return self.card_repository.get_by_deck_id(deck_id=deck_id)
        except DeckNotFoundError as err:
            raise err

    def decks_list(self) -> list[Deck]:
        return self.deck_repository.get_all()
    
    def delete(self, deck_id: UUID):
        self.deck_repository.delete(deck_id)

    # def draw_card(self) -> Card:
    #     next_card = self.card_repository.get_next(deck_id, "deu")
    #     if not next_card:
    #         next_card.card_repository.get_next(deck_id, "learn")
    #     if not next_card:
    #         next_card.card_repository.get_next(deck_id, "new")


class TemplateService():
    template_repository: TemplateRepositoryInterface

    def __init__(self, request: Request):
        self.template_repository = request.app.config.repositories.templates

    def template_list(self) -> list[UUID]:
        return self.template_repository.get_all()
