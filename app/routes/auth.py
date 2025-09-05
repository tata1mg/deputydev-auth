from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth.auth_factory import AuthFactory
from app.services.auth.signup.signup_service import SignUp
from app.utils import authenticate

auth_route = APIRouter()


@auth_route.get("/get-auth-data", summary="Get auth data endpoint", description="Returns auth data")
async def get_auth_data(_request: Request) -> JSONResponse:
    response = await authenticate.get_auth_data(_request)
    return JSONResponse(response)


@auth_route.get("/get-session", summary="Get session endpoint", description="Returns session data")
async def get_session(_request: Request) -> JSONResponse:
    headers = _request.headers
    auth_provider = AuthFactory.get_auth_provider()
    response = await auth_provider.get_auth_session(headers)
    return JSONResponse(response.model_dump(mode="json"))


@auth_route.post("/sign-up", summary="Sign up endpoint", description="Sign up a new user")
async def sign_up(_request: Request) -> JSONResponse:
    headers = _request.headers
    response = await SignUp.signup(headers)
    return JSONResponse(response)


@auth_route.post("/verify-auth-token", summary="Verify auth token endpoint", description="Verify auth token")
async def verify_auth_token(_request: Request) -> JSONResponse:
    auth_provider = AuthFactory.get_auth_provider()
    response = await auth_provider.extract_and_verify_token(_request)
    return JSONResponse(response.model_dump(mode="json"))
