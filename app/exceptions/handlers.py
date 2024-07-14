from typing import Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import (
    CardErrorException,
    CardNotFoundException,
    DeckErrorException,
    DeckNotFoundException,
)


async def error_handler(
    request: Request,
    exc: Union[HTTPException, Exception],
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


def add_exeption_handlers(app: FastAPI):
    app.add_exception_handler(CardErrorException, error_handler)
    app.add_exception_handler(DeckErrorException, error_handler)
    app.add_exception_handler(CardNotFoundException, error_handler)
    app.add_exception_handler(DeckNotFoundException, error_handler)
