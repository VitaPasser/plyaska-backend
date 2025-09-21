from logging import Logger

from src.controllers.Home import Home
from src.controllers.PostEventCRUD import PostEventCRUD
from src.controllers.PromotionCRUD import PromotionCRUD
from src.controllers.UserCRUD import UserCRUD
from src.repositories.PostEventRepository import PostEventRepository
from src.services.PostEventService import PostEventService
from src.services.PromotionService import PromotionService
from src.utils.db.DBProvider import DBProvider


def provider_register(logger: Logger, database: DBProvider):
    providers = [Home(),
                 PostEventCRUD(
                     logger=logger,
                     post_event_service=PostEventService(
                         logger=logger,
                         database=database,
                         promotion_service=PromotionService(logger, database),
                         post_event_repository=PostEventRepository(logger, database)
                     ),
                     promotion_service=PromotionService(logger, database)
                 ),
                 PromotionCRUD(
                     promotion_service=PromotionService(logger, database)
                 ),
                 UserCRUD(logger=logger)]
    return providers
