from typing import Any, Dict, List, Optional, Union

from fastapi.logger import logger

from app.models.dao.postgres.users import Users
from app.models.dto.user_dto import UserDTO


class UserRepository:
    @classmethod
    async def db_get(cls, filters: Dict[str, Any], fetch_one: bool = False) -> Optional[Union[UserDTO, List[UserDTO]]]:
        """
        Fetch user(s) from the database.
        """
        try:
            if fetch_one:
                user = await Users.get_or_none(**filters)
                return UserDTO.model_validate(user.__dict__) if user else None
            else:
                users = await Users.filter(**filters).all()
                return [UserDTO.model_validate(user.__dict__) for user in users]

        except Exception as ex:
            logger.error(f"Error occurred while fetching user(s) from db with filters: {filters}", exc_info=True)
            raise ex
