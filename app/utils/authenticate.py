from datetime import datetime, timezone
from typing import Any, Dict, Union

from fastapi import Request

from app.common.dataclasses.main import AuthData, AuthSessionData, AuthStatus, SubscriptionStatus
from app.models.dto.user_team_dto import UserTeamDTO
from app.repository.subscriptions.subscriptions_repository import SubscriptionsRepository
from app.repository.user_teams.user_team_repository import UserTeamRepository
from app.repository.users.user_repository import UserRepository
from app.services.auth_factory import AuthFactory
from app.services.signup.signup_service import SignUp


async def get_auth_data(request: Request) -> Dict[str, Union[AuthData, Dict[str, Any]]]:
    """
    Get the auth data from the request
    """
    response_headers = {}
    auth_provider = AuthFactory.get_auth_provider()
    verification_result: AuthSessionData = await auth_provider.extract_and_verify_token(request)

    if verification_result.status == AuthStatus.NOT_VERIFIED:
        raise Exception(verification_result.error_message or AuthStatus.NOT_VERIFIED.value)

    if verification_result.status == AuthStatus.EXPIRED:
        response_headers = {"new_session_data": verification_result.encrypted_session_data}

    # Extract the email from the user response
    email = verification_result.user_email
    if not email:
        raise ValueError("Email not found in session data")

    # Fetch the user ID based on the email
    user = await UserRepository.db_get(filters={"email": email}, fetch_one=True)
    user_id = user.id

    # If the user ID is not found, raise an error
    if not user_id:
        raise ValueError("User not found")

    # Get the team ID based on the email domain
    team_info = await SignUp.get_team_info_from_email(email)
    team_id = team_info.get("team_id")

    # If the team ID is not found, raise an error
    if not team_id:
        raise ValueError("Team not found")

    # Fetch the user team ID based on the user ID and team ID
    user_team: UserTeamDTO = await UserTeamRepository.db_get(
        filters={"user_id": user_id, "team_id": team_id}, fetch_one=True
    )
    user_team_id = user_team.id

    # If the user team ID is not found, raise an error
    if not user_team_id:
        raise ValueError("User team not found")

    # Check subscription
    subscription = await SubscriptionsRepository.get_by_user_team_id(user_team_id)
    if not subscription:
        raise ValueError("Subscription not found")

    # Check subscription expiry
    if subscription.end_date is not None and (
        subscription.end_date < datetime.now(timezone.utc)
        or SubscriptionStatus(subscription.current_status) != SubscriptionStatus.ACTIVE
    ):
        raise Exception("Subscription expired")

    # prepare the auth data
    auth_data = None
    if response_headers and response_headers["new_session_data"]:
        auth_data = AuthData(user_team_id=user_team_id, session_refresh_token=response_headers["new_session_data"])
    else:
        auth_data = AuthData(user_team_id=user_team_id)

    return {"auth_data": auth_data.model_dump(mode="json"), "response_headers": response_headers}
