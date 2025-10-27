from datetime import datetime
from typing import TYPE_CHECKING, Tuple

from beanie import PydanticObjectId
from bson import SON

from src.models.post_event import PostEvent
from src.utils.models.data_to_objects import CreateSchemaT, UpdateSchemaT
from src.utils.repositories.beanie_auto_crud_repository import BeanieAutoCRUDRepository

__repository = BeanieAutoCRUDRepository(PostEvent)

__all__ = [f for f in __repository.export_methods().keys()]

if TYPE_CHECKING:

    async def create(item: CreateSchemaT | PostEvent) -> PostEvent: ...
    async def update_or_error(
        _id: PydanticObjectId, item: UpdateSchemaT | PostEvent
    ) -> PostEvent: ...
    async def update_or_create(
        _id: PydanticObjectId, item: UpdateSchemaT | PostEvent
    ) -> PostEvent: ...
    async def find_all() -> list[PostEvent]: ...
    async def find_by_id(_id: PydanticObjectId) -> PostEvent: ...
    async def find_by_id_or_error(_id: PydanticObjectId) -> PostEvent: ...
    async def delete(_id: PydanticObjectId) -> PostEvent: ...


async def find_near_post_events(
    max_distance_in_meters: int, coordinates: Tuple[float, float]
):
    now = datetime.now()
    return await PostEvent.aggregate(
        [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": coordinates},
                    "distanceField": "distance",
                    "maxDistance": max_distance_in_meters,
                    "spherical": True,
                }
            },
            {
                "$addFields": {
                    # Отберём только активные промоции
                    "active_promotions": {
                        "$filter": {
                            "input": "$promotions",
                            "as": "promotions",
                            "cond": {
                                "$and": [
                                    {"$gt": ["$$promotions.promotion_type.power", 0]},
                                    {"$lte": ["$$promotions.start_datetime", now]},
                                    {"$gt": ["$$promotions.end_datetime", now]},
                                ]
                            },
                        }
                    }
                }
            },
            {
                "$addFields": {
                    # Посчитаем score = min(distance / power) по всем активным
                    "score": {
                        "$cond": [
                            {"$gt": [{"$size": "$active_promotions"}, 0]},
                            {
                                "$reduce": {
                                    "input": {
                                        "$map": {
                                            "input": "$active_promotions",
                                            "as": "ap",
                                            "in": {
                                                "$divide": [
                                                    {"$add": ["$distance", 1]},
                                                    "$$ap.promotion_type.power",
                                                ]
                                            },
                                        }
                                    },
                                    "initialValue": float(
                                        "inf"
                                    ),  # стартовое большое число
                                    "in": {"$min": ["$$value", "$$this"]},
                                }
                            },
                            # Если активных нет — просто расстояние
                            {"$add": ["$distance", 1]},
                        ]
                    }
                }
            },
            {"$sort": SON([("score", 1)])},
            {"$limit": 10000},
        ]
    ).to_list()
