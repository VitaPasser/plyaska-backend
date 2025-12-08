from datetime import datetime

from beanie import PydanticObjectId
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from src import repositories
from src.exceptions.errors.repository import NotFoundedError
from src.models.post_event import PromotionDeal
from src.models.promotion import Promotion


async def create_deal(promotion: Promotion):
    end_datetime = datetime.now() + relativedelta(seconds=promotion.duration)
    start_datetime = datetime.now()
    promotion_deal = PromotionDeal(
        promotion_type=promotion,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
    )
    return promotion_deal


async def find_by_id(promotion_id: PydanticObjectId):
    try:
        return await repositories.promotion.find_by_id_or_error(promotion_id)
    except NotFoundedError:
        raise HTTPException(status_code=404, detail="Not found")
