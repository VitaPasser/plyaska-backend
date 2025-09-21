from datetime import datetime
from typing import Tuple

from bson import SON

from src.models.PostEvent import PostEvent
from src.utils.repository.BaseRepository import BaseRepository


class PostEventRepository(BaseRepository):
    def __init__(self, logger, database):
        super().__init__(logger, database)

    async def find_near_post_events(self, max_distance_in_meters: int,
                                    coordinates: Tuple[float, float]):
        now = datetime.now()
        return await PostEvent.aggregate(
            [
                {
                    "$geoNear": {
                        "near": {"type": "Point", "coordinates": coordinates},
                        "distanceField": "distance",
                        "maxDistance": max_distance_in_meters,
                        "spherical": True
                    }
                },
                {"$unwind": {"path": "$promotions", "preserveNullAndEmptyArrays": True}},
                {"$addFields": {
                    "score": {
                        "$cond": [
                            {"$and": [
                                {"$gt": ["$promotions.promotion_type.power", 0]},
                                {"$gt": ["$promotions.end_datetime", now]},
                                {"$lte": ["$promotions.start_datetime", now]},
                            ]},
                            {"$divide": ["$distance", "$promotions.promotion_type.power"]},
                            "$distance"
                        ]
                    }
                }},
                {"$sort": SON([("score", 1)])},
                {"$limit": 10000}
            ]
        ).to_list()
