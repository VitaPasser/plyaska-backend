from datetime import timedelta, datetime
from decimal import Decimal
from logging import Logger

from dateutil.relativedelta import relativedelta

from src.models.PostEvent import PromotionDeal
from src.models.Promotion import Promotion, Money
from src.utils.service.BaseService import BaseService
from src.utils.db.DBProvider import DBProvider


class PromotionService(BaseService):

    def __init__(self, logger: Logger, database: DBProvider):
        super().__init__(logger, database)

    async def create_deal(self, promotion: Promotion):
        end_datetime = datetime.now() + relativedelta(seconds=promotion.duration)
        start_datetime = datetime.now()
        promotion_deal = PromotionDeal(promotion_type=promotion,
                                       start_datetime=start_datetime,
                                       end_datetime=end_datetime)
        return promotion_deal


    async def create(self):
        promotion = Promotion(name="Super Sale", description="50% off for first month",
                              power=Decimal("20000000"),
                              duration=int(timedelta(days=30).total_seconds()),
                              price=Money(amount=Decimal("9.99"), currency="USD"))
        return await promotion.insert()

    async def find_by_id(self, promotion_id):
        return await Promotion.find_one(Promotion.id == promotion_id)

    async def find_all(self):
        return await Promotion.find_all().to_list()
