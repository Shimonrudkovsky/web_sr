from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.repository.interfaces import RepositoryError
from app.core.service import CardService, DeckService
from app.exceptions.exceptions import CardNotFoundException, DeckErrorException, DeckNotFoundException
from app.schemas.request import NewDeckRequest
from app.schemas.response import BaseExeptionResponse, CardResponse, DeckResponse

deck_router = APIRouter()


@deck_router.get(
    "/decks",
    response_model=list[DeckResponse],
    responses={
        200: {"description": "Successful Response"},
        404: {"decription": "Deck not found", "model": BaseExeptionResponse},
    },
)
def get_decks(
    deck_service: DeckService = Depends(DeckService),
) -> list[DeckResponse]:
    try:
        deck_list = deck_service.decks_list()
    except RepositoryError as err:
        raise DeckNotFoundException(message=err.message)

    if deck_list == []:
        raise DeckNotFoundException(message="empty deck list")

    return [DeckResponse(**deck.model_dump()) for deck in deck_list]


@deck_router.post(
    "/deck",
    response_model=UUID,
    responses={
        200: {"description": "Successful Response"},
        400: {"description": "Unable to create deck", "model": BaseExeptionResponse},
    },
)
def new_deck(new_deck: NewDeckRequest, deck_service: DeckService = Depends(DeckService)) -> UUID:
    try:
        new_deck_id = deck_service.new_deck(name=new_deck.name)
    except RepositoryError as err:
        raise DeckErrorException(message=f"deck creation error: {err.message}")

    return new_deck_id


@deck_router.get(
    "/deck/{deck_id}",
    response_model=list[UUID],
    responses={
        200: {"description": "Successful Response"},
        404: {"decription": "Deck not found", "model": BaseExeptionResponse},
    },
)
def get_deck_info(
    deck_id: UUID,
    deck_service: DeckService = Depends(DeckService),
) -> list[UUID]:
    try:
        deck_info = deck_service.get_deck_info(deck_id=deck_id)
    except RecursionError:
        raise DeckNotFoundException(message=str(deck_id))

    return deck_info


@deck_router.delete(
    "/deck/{deck_id}",
    responses={
        200: {"description": "Successful Response"},
        400: {"description": "Unable to create deck", "model": BaseExeptionResponse},
    },
)
def delete_deck(
    deck_id: UUID,
    deck_service: DeckService = Depends(DeckService),
) -> str:
    try:
        deck_service.delete(deck_id=deck_id)
    except RepositoryError as err:
        raise DeckErrorException(message=f"deck deletion error: {err.message}")

    return "ok"


@deck_router.get(
    "/deck/{deck_id}/next_card",
    response_model=CardResponse,
    responses={
        200: {"description": "Successful Response"},
        404: {"decription": "Deck not found", "model": BaseExeptionResponse},
    },
)
def draw_card(deck_id: UUID, card_service: CardService = Depends(CardService)) -> CardResponse:
    try:
        return card_service.get_next_due(deck_id=deck_id)
    except RepositoryError as err:
        raise CardNotFoundException(message=err.message)
