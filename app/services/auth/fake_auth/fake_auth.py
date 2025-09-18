from datetime import datetime
from typing import Dict

from app.common.dataclasses.main import AuthSessionData, AuthStatus, GraceConfig
from app.models.dao.postgres.subscription_plans import SubscriptionPlans
from app.models.dao.postgres.subscriptions import Subscriptions
from app.models.dao.postgres.teams import Teams
from app.models.dao.postgres.user_teams import UserTeams
from app.models.dao.postgres.users import Users
from app.repository.users.user_repository import UserRepository
from app.services.auth.base_auth import BaseAuth
from app.utils.config_manager import ConfigManager


class FakeAuth(BaseAuth):
    async def _create_user_if_not_exists(self) -> None:
        # Check if FAKE user is in DB, if not create one
        fake_user = await UserRepository.db_get(
            filters={"email": ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"]}, fetch_one=True
        )
        if not fake_user:
            user = await Users.create(
                name=ConfigManager.configs()["FAKE_AUTH"]["USER_NAME"],
                email=ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"],
                org_name=ConfigManager.configs()["FAKE_AUTH"]["USER_ORG_NAME"],
            )
            fake_user = user

        fake_team = await Teams.filter(name=ConfigManager.configs()["FAKE_AUTH"]["USER_ORG_NAME"]).first()
        if not fake_team:
            team = await Teams.create(
                name=ConfigManager.configs()["FAKE_AUTH"]["USER_ORG_NAME"],
            )
            fake_team = team

        fake_user_team = await UserTeams.filter(user_id=fake_user.id, team_id=fake_team.id).first()
        if not fake_user_team:
            user_team = await UserTeams.create(
                user_id=fake_user.id,
                team_id=fake_team.id,
                role="admin",
                is_owner=True,
                is_billable=False,
                last_pr_authored_or_reviewed_at=datetime.now(),
            )
            fake_user_team = user_team

        fake_subscription = await Subscriptions.filter(user_team_id=fake_user_team.id).first()
        if not fake_subscription:
            fake_subscription_plan = await SubscriptionPlans.filter(
                plan_type=ConfigManager.configs()["FAKE_AUTH"].get("SUBSCRIPTION_PLAN", "free")
            ).first()
            if not fake_subscription_plan:
                fake_subscription_plan = await SubscriptionPlans.create(
                    plan_type=ConfigManager.configs()["FAKE_AUTH"].get("SUBSCRIPTION_PLAN", "free")
                )
            await Subscriptions.create(
                plan_id=fake_subscription_plan.id,
                user_team_id=fake_user_team.id,
                current_status="ACTIVE",
                start_date=datetime.now(),
            )

    async def get_auth_session(self, headers: Dict[str, str]) -> AuthSessionData:
        # Check if FAKE user is in DB, if not create one
        await self._create_user_if_not_exists()
        return AuthSessionData(
            status=AuthStatus.AUTHENTICATED,
            user_email=ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"],
            user_name=ConfigManager.configs()["FAKE_AUTH"]["USER_NAME"],
            encrypted_session_data=ConfigManager.configs()["FAKE_AUTH"]["ENCRYPTED_SESSION_DATA"],
        )

    async def extract_and_verify_token(self, grace_config: GraceConfig, headers: Dict[str, str]) -> AuthSessionData:
        # Check if FAKE user is in DB, if not create one
        await self._create_user_if_not_exists()
        return AuthSessionData(
            status=AuthStatus.VERIFIED,
            user_email=ConfigManager.configs()["FAKE_AUTH"]["USER_EMAIL"],
            user_name=ConfigManager.configs()["FAKE_AUTH"]["USER_NAME"],
            encrypted_session_data=ConfigManager.configs()["FAKE_AUTH"]["ENCRYPTED_SESSION_DATA"],
        )
