from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fsrs import Rating
from fsrs.models import SchedulingInfo

from app.core.repository.interfaces import CardNotFoundError, RepositoryError
from app.core.service import CardService
from app.exceptions.exceptions import CardErrorException, CardNotFoundException, UnknownRatingException
from app.schemas.request import NewCardrequest, RateCardRequest
from app.schemas.response import BaseExeptionResponse, CardResponse

card_router = APIRouter()


@card_router.post(
    "/card",
    response_model=UUID,
    responses={
        200: {"description": "Successful Response"},
        400: {"description": "Can't create new card", "model": BaseExeptionResponse},
    },
)
async def new_card(
    new_card: NewCardrequest,
    card_service: CardService = Depends(CardService),
) -> UUID:
    try:
        new_card_id = await card_service.new_card(new_card.template_id, new_card.deck_id, new_card.fields)
    except RepositoryError as err:
        raise CardNotFoundException(message=err.message)

    return new_card_id


@card_router.get(
    "/card/{card_id}",
    response_model=CardResponse,
    responses={
        200: {"description": "Successful Response"},
        404: {"description": "Card not found", "model": BaseExeptionResponse},
    },
)
async def get_card(
    card_id: UUID,
    card_service: CardService = Depends(CardService),
) -> CardResponse:
    try:
        return await card_service.get_card_response(card_id)
    except CardNotFoundError as err:
        raise CardNotFoundException(message=err.message)


@card_router.put(
    path="/card/{card_id}/rating",
    responses={
        200: {"description": "Successful Response"},
        400: {"description": "Can't rate card", "model": BaseExeptionResponse},
        404: {"description": "Card not found", "model": BaseExeptionResponse},
    },
)
async def rate(
    card_id: UUID, request: Request, request_body: RateCardRequest, card_service: CardService = Depends(CardService)
) -> str:
    try:
        card = await card_service.get_card(card_id)
    except CardNotFoundError as err:
        raise CardNotFoundException(message=err.message)
    now = datetime.now(timezone.utc)
    review_results = request.app.config.fsrs.repeat(card, now)

    reviewed_card: SchedulingInfo = None
    if request_body.rating == Rating.Again:
        reviewed_card = review_results[Rating.Again]
    elif request_body.rating == Rating.Hard:
        reviewed_card = review_results[Rating.Hard]
    elif request_body.rating == Rating.Good:
        reviewed_card = review_results[Rating.Good]
    elif request_body.rating == Rating.Easy:
        reviewed_card = review_results[Rating.Easy]
    else:
        raise UnknownRatingException(message=str(request_body.rating))

    try:
        await card_service.update(scheduled_card=reviewed_card)
    except RepositoryError as err:
        raise CardErrorException(message=f"card update error: {err.message}")

    return "ok"
