from typing import Optional

from fastapi.logger import logger

from app.models.dao.postgres.referral_codes import ReferralCodes
from app.models.dto.referral_codes_dto import ReferralCodeDTO


class ReferralCodesRepository:
    @classmethod
    async def get_by_code(cls, referral_code: str) -> Optional[ReferralCodeDTO]:
        try:
            filters = {"referral_code": referral_code}
            referral_code = await ReferralCodes.get_or_none(**filters)
            return ReferralCodeDTO.model_validate(referral_code) if referral_code else None
        except Exception as ex:
            logger.error(f"Error occurred while fetching referral code from db with filters: {filters}", exc_info=True)
            raise ex
