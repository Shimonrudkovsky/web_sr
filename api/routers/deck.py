from uuid import UUID, uuid4
from fastapi import APIRouter, Depends
from schemas.request import NewDeckRequest
from schemas.response import DeckResponse, CardResponse
from core.repository.interfaces import RepositoryError
from core.service import DeckService, CardService


deck_router = APIRouter()

@deck_router.get("/decks", response_model=list[DeckResponse])
def get_decks(
    deck_service: DeckService = Depends(DeckService),
) -> list[DeckResponse]:
    return deck_service.decks_list()

@deck_router.post("/deck", response_model=UUID)
def new_deck(
    new_deck: NewDeckRequest,
    deck_service: DeckService = Depends(DeckService)
) -> UUID:
    try:
        new_deck_id = deck_service.new_deck(name=new_deck.name)
    except RepositoryError as err:
        raise err
    
    return new_deck_id

@deck_router.get("/deck/{deck_id}", response_model=list[UUID])
def get_deck_info(
    deck_id: UUID,
    deck_service: DeckService = Depends(DeckService),
    card_service: CardService = Depends(CardService),
) -> list[CardResponse]:
    return  deck_service.get_deck_info(deck_id=deck_id)

@deck_router.delete("/deck/{deck_id}")
def delete_deck(
    deck_id: UUID,
    deck_service: DeckService = Depends(DeckService),
) -> str:
    deck_service.delete(deck_id=deck_id)

    return "ok"
