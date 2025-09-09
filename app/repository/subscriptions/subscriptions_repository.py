from typing import Optional

from fastapi.logger import logger

from app.models.dao.postgres.subscriptions import Subscriptions
from app.models.dto.subscriptions_dto import SubscriptionDTO


class SubscriptionsRepository:
    @classmethod
    async def get_by_user_team_id(cls, user_team_id: int) -> Optional[SubscriptionDTO]:
        try:
            filters = {"user_team_id": user_team_id}
            subscription = await Subscriptions.get_or_none(**filters)
            return SubscriptionDTO.model_validate(subscription.__dict__) if subscription else None
        except Exception as ex:
            logger.error(
                f"Error occurred while getting subscription by user team id {user_team_id} from DB", exc_info=True
            )
            raise ex
