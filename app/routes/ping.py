from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

ping_route = APIRouter()

@ping_route.get("/ping", summary="Health Check", description="Returns pong")
async def ping(_request: Request) -> JSONResponse:
    return JSONResponse({"message": "pong"})