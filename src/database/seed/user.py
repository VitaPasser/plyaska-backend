import asyncio

import faker

from src.main import main
from src.models.user import User


async def seed_user():
    await main.setup()
    fake = faker.Faker()

    for _ in range(100):
        user = User(
            username=fake.user_name(), email=fake.email(), full_name=fake.name()
        )
        await user.insert()


if __name__ == "__main__":
    asyncio.run(seed_user())
