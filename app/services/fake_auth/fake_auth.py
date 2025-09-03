from typing import Any, Dict

from app.services.base_auth import BaseAuth
from app.utils.config_manager import ConfigManager
from app.utils.dataclasses.main import AuthSessionData, AuthStatus


class FakeAuth(BaseAuth):
    async def get_auth_session(self, headers: Dict[str, str]) -> AuthSessionData:
        return AuthSessionData(
            status=AuthStatus.AUTHENTICATED,
            user_email=ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"],
            user_name=ConfigManager.configs()["FAKE_AUTH"]["USER_NAME"],
            encrypted_session_data=ConfigManager.configs()["FAKE_AUTH"]["ENCRYPTED_SESSION_DATA"],
        )

    async def extract_and_verify_token(self, request: Dict[str, Any]) -> AuthSessionData:
        return AuthSessionData(
            status=AuthStatus.VERIFIED,
            user_email=ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"],
            user_name=ConfigManager.configs()["FAKE_AUTH"]["USER_NAME"],
            encrypted_session_data=ConfigManager.configs()["FAKE_AUTH"]["ENCRYPTED_SESSION_DATA"],
        )
