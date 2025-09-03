from fastapi import APIRouter
from fastapi.responses import JSONResponse

auth_route = APIRouter()


@auth_route.get("/auth", summary="Auth endpoint", description="Returns auth message to confirm service is running")
async def auth() -> JSONResponse:
    return {"message": "auth message"}
