from fastapi import APIRouter

from app.services.pong import Pong

ping_route = APIRouter()


@ping_route.get("/ping", summary="Ping endpoint", description="Returns pong to confirm service is running")
async def ping():
    pong = Pong()
    return pong.get_message()
