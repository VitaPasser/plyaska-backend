import asyncio
import os
from datetime import datetime, timedelta
from decimal import Decimal

from beanie import init_beanie
from beanie.operators import Near
from bson import SON
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient, AsyncMongoClient

from src.models.PostEvent import PostEvent, User, Image, Location, PromotionDeal
from src.models.Promotion import Promotion, Money


def get_mongo_url():
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    return f"mongodb://{mongo_username}:{mongo_password}@mongodb:27017"


async def example():
    try:
        client = AsyncMongoClient(get_mongo_url())
        await init_beanie(database=client.plyaska_db, document_models=[PostEvent, Promotion])
        await PostEvent.delete_all()
        await Promotion.delete_all()
        now = datetime.now()

        print("MongoDB connected successfully")
        promotion = Promotion(name="Super Sale", description="50% off for first month",
                              power=Decimal("20000000"),
                              duration=int(timedelta(days=30).total_seconds()),
                              price=Money(amount=Decimal("9.99"), currency="USD"))
        print(f"Promotion before insert: {promotion}")
        await promotion.insert()
        promotion = await Promotion.find_one(Promotion.name == "Super Sale")
        print(promotion)

        end_datetime = now - relativedelta(seconds=promotion.duration)
        start_datetime = end_datetime - relativedelta(seconds=promotion.duration)
        promotion_deal = PromotionDeal(promotion_type=promotion, start_datetime=start_datetime,
                                       end_datetime=end_datetime)

        author = User(username="user1", email="user1@gmail.com", full_name="User One")
        image1 = Image(url="http://example.com/image1.jpg", description="An example image")
        image2 = Image(url="http://example.com/image2.jpg", description="An example image two")
        location = Location(coordinates=(37.6173, 55.7558))
        post_event = PostEvent(
            name="Sample Event",
            description="This is a sample event description.",
            author=author,
            images=[image1, image2],
            location=location,
            promotions=[promotion_deal]
        )
        await post_event.insert()

        author = User(username="user2", email="user1@gmail.com", full_name="User Two")
        location = Location(coordinates=(59.6173, 59.7558))
        post_event = PostEvent(
            name="Sample Event",
            description="This is a sample event description.",
            author=author,
            images=[image1, image2],
            location=location
        )
        await post_event.insert()

        post_event_searched = await PostEvent.find_one(PostEvent.author.username == "user2")
        print(f"Post event searched: {post_event_searched}")

        await post_event.set({PostEvent.name: "Polytech event in basement"})

        post_event_searched = await PostEvent.aggregate(
            [
                {
                    "$geoNear": {
                        "near": {"type": "Point", "coordinates": [50.6173, 58.7558]},
                        "distanceField": "distance",
                        "maxDistance": 8000000,  # in meters
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
        print(f"Post event searched by geometry and after update: {post_event_searched}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


def main():
    print("Hello from plyaska-backend!")

    try:
        client = MongoClient(get_mongo_url())
        print(f"MongoDB URL: {get_mongo_url()}")
        db = client["plyaska_db"]
        print(f"DB name: {db.name}")
        db.post_event.insert_one(
            {"name": "В ПОДВАЛЕ ПОЛИТЕХА ДЕРЖАТ НАС! ПОМОГИТЕ!", "description": "ПОМОГИТЕ!", "date": "2024-06-01",
             "author": "Девочка1 из подвала"})
        db.post_event.insert_one(
            {"name": "В ПОДВАЛЕ ПОЛИТЕХА ДЕРЖАТ НАС2! ПОМОГИТЕ!", "description": "ПОМОГИТЕ!", "date": "2024-06-02",
             "author": "Девочка2 из подвала"})
        db.post_event.insert_one(
            {"name": "В ПОДВАЛЕ ПОЛИТЕХА ДЕРЖАТ НАС3! ПОМОГИТЕ!", "description": "ПОМОГИТЕ!", "date": "2024-06-03",
             "author": "Девочка2 из подвала"})
        post_event = db.post_events.find_one({"author": "Девочка1 из подвала"})
        print(f"Post event: {post_event}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")


if __name__ == "__main__":
    main()
    asyncio.run(example())
