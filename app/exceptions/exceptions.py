from fastapi import HTTPException


class CardErrorException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, detail=f"card error: {message}")


class DeckErrorException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, detail=f"deck error: {message}")


class CardNotFoundException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=404, detail=f"card not found: {message}")


class DeckNotFoundException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=404, detail=f"deck not found: {message}")


class UnknownRatingException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=400, detail=f"unknown rating: {message}")
