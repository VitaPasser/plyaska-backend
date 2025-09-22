from datetime import datetime

from beanie import PydanticObjectId
from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from src.models.PostEvent import PromotionDeal
from src.models.Promotion import Promotion


async def create_deal(promotion: Promotion):
    end_datetime = datetime.now() + relativedelta(seconds=promotion.duration)
    start_datetime = datetime.now()
    promotion_deal = PromotionDeal(promotion_type=promotion,
                                   start_datetime=start_datetime,
                                   end_datetime=end_datetime)
    return promotion_deal


async def find_by_id(promotion_id: PydanticObjectId):
    promotion = await Promotion.get(promotion_id)
    if promotion is None:
        raise HTTPException(status_code=404, detail="Not found")
    return promotion
