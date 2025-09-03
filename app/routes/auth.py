from fastapi import APIRouter

auth_route = APIRouter()


@auth_route.get("/auth", summary="Auth endpoint", description="Returns auth message to confirm service is running")
async def auth():
    return {"message": "auth message"}
