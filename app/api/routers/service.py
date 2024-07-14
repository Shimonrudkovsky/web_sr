from fastapi import APIRouter

service_router = APIRouter()


@service_router.get("/ping")
def home() -> dict:
    return {"message": "pong"}
