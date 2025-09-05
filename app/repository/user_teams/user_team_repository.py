from typing import Any, Dict, List, Union

from fastapi.logger import logger

from app.models.dao.postgres.user_teams import UserTeams
from app.models.dto.user_team_dto import UserTeamDTO


class UserTeamRepository:
    @classmethod
    async def db_get(
        cls, filters: Dict[str, Any], fetch_one: bool = False
    ) -> Union[UserTeamDTO, List[UserTeamDTO]] | None:
        try:
            if fetch_one:
                user_team = await UserTeams.get_or_none(**filters)
                return UserTeamDTO.model_validate(user_team.__dict__) if user_team else None
            else:
                user_teams = await UserTeams.filter(**filters).all()
                return [UserTeamDTO.model_validate(user_team.__dict__) for user_team in user_teams]

        except Exception as ex:
            logger.error(
                f"Error occurred while fetching user_team details with filters: {filters} from db for user_team",
                exc_info=True,
            )
            raise ex
