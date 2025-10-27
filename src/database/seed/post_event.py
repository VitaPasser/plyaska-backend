import asyncio
import random

import faker

from src.main import main
from src.models.post_event import Image, Location, PostEvent
from src.models.user import User


async def seed_post_event():
    await main.setup()
    fake = faker.Faker()

    for _ in range(300):
        user_dict = (await User.aggregate([{"$sample": {"size": 1}}]).to_list())[0]
        user = User.model_validate(user_dict)
        images = [
            Image(url=fake.image_url(), description=fake.sentence())
            for _ in range(random.randint(1, 10))
        ]
        post_event = PostEvent(
            name=fake.sentence(),
            description=" ".join(fake.sentences(5)),
            author=user,
            images=images,
            location=Location(
                coordinates=(float(fake.longitude()), float(fake.latitude()))
            ),
            # promotions=...,
        )

        await post_event.insert()


if __name__ == "__main__":
    asyncio.run(seed_post_event())
