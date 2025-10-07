from datetime import datetime
from typing import Tuple

from bson import SON

from src.models.post_event import PostEvent


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
                                                    "$distance",
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
                            "$distance",
                        ]
                    }
                }
            },
            {"$sort": SON([("score", 1)])},
            {"$limit": 10000},
        ]
    ).to_list()
