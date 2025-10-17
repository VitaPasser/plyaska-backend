import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.models.promotion import Promotion
from src.utils.test_utils.other import output_response
from src.utils.test_utils.response_models import ResponseDo, ResponseModel


@pytest_asyncio.fixture
async def create_promotion(client: AsyncClient) -> ResponseDo:
    async def _create_promotion() -> ResponseModel:
        response = await client.post(
            url="/promotions/",
            content="""
                    {
                      "name": "Test promotion",
                      "description": "It's just test promotion",
                      "power": 100,
                      "duration": 480,
                      "price": {
                        "amount": 100,
                        "currency": "USD"
                      }
                    }
                    """,
        )
        assert response.status_code == 201, output_response(response)
        model = Promotion(**response.json())
        return ResponseModel(response=response, model=model)

    promotion = await _create_promotion()
    return ResponseDo(response=promotion.response, model=promotion.model, do=_create_promotion)


@pytest.mark.asyncio
async def test_create(client: AsyncClient, create_promotion: ResponseDo):
    response = create_promotion.response
    assert response.status_code == 201, response.json()


@pytest.mark.asyncio
async def test_find_all(client: AsyncClient, create_promotion: ResponseDo):
    models_test = [(await create_promotion.do()).model, (await create_promotion.do()).model]
    response = await client.get(url="/promotions/")

    assert response.status_code == 200, response.json()

    models = [Promotion.model_validate(promotion) for promotion in response.json()]

    assert {m.id for m in models} >= {m.id for m in models_test}, response.json()


@pytest.mark.asyncio
async def test_find_by_id(client: AsyncClient, create_promotion: ResponseDo):
    _id = create_promotion.response.json()["_id"]
    response = await client.get(url=f"/promotions/{_id}")
    assert response.status_code == 200, response.json()


@pytest.mark.asyncio
async def test_update(client: AsyncClient, create_promotion: ResponseDo):
    _id = (await create_promotion.do()).model.id
    response = await client.patch(
        url=f"/promotions/{_id}",
        content="""
                {
                  "power": 120,
                  "price": {
                    "amount": 200
                  }
                }
                """,
    )
    assert response.status_code == 200, response.json()
    model = Promotion.model_validate(response.json())
    assert (model.updated_at is not None
            and model.created_at is not None
            and model.price.currency is not None), response.json()


@pytest.mark.asyncio
async def test_delete(client: AsyncClient, create_promotion: ResponseDo):
    _id = (await create_promotion.do()).model.id
    response = await client.delete(url=f"/promotions/{_id}")
    assert response.status_code == 200, response.json()
