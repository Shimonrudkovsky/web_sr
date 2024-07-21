from fastapi import APIRouter

service_router = APIRouter()


@service_router.get("/ping")
def ping() -> dict:
    return {"message": "pong"}
