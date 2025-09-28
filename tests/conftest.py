from typing import AsyncGenerator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport

from src.main import main


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(main.app):
        async with AsyncClient(
                transport=ASGITransport(app=main.app),
                base_url="http://test",
        ) as client:
            yield client