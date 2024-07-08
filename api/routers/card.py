from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, Request
from fastapi import status

from core.service import CardService, DeckService
from schemas.response import CardResponse
from schemas.request import RateCardRequest, NewCardrequest


card_router = APIRouter()


@card_router.post("/card", response_model=UUID)
def new_card(
    new_card: NewCardrequest,
    card_service: CardService = Depends(CardService),
) -> UUID:
    new_card_id = card_service.new_card(new_card.template_id, new_card.deck_id, new_card.fields)

    return new_card_id


@card_router.get("/card/{card_id}", response_model=CardResponse)
def get_card(
    card_id: UUID,
    card_service: CardService = Depends(CardService),
    deck_service: DeckService = Depends(DeckService),
) -> CardResponse:
    return card_service.get_card_response(card_id)


@card_router.put("/card/{card_id}/rate")
def rate(
    card_id: UUID,
    request: Request,
    request_body: RateCardRequest,
    card_service: CardService = Depends(CardService)
) -> str:
    card = card_service.get_card(card_id)
    print(f"!!!!!!!!{card.id}: {request_body.rate}")

    return "ok"
