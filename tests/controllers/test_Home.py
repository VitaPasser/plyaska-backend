import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get(url="/")
    print(response)
    assert response.status_code == 200
