import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.models.user import User
from src.utils.tests.other import output_response
from src.utils.tests.response_models import ResponseDo, ResponseModel


@pytest_asyncio.fixture
async def create_user(client: AsyncClient) -> ResponseDo:
    async def _create_user() -> ResponseModel:
        response = await client.post(
            url="/users/",
            content="""
                    {
                       "username": "123",
                       "email": "abc@gmail.com",
                       "full_name": "123"
                    }
                    """,
        )
        assert response.status_code == 201, output_response(response)
        model = User(**response.json())
        return ResponseModel(response=response, model=model)

    user = await _create_user()
    return ResponseDo(response=user.response, model=user.model, do=_create_user)


@pytest.mark.asyncio
async def test_create(client: AsyncClient, create_user: ResponseDo):
    response = create_user.response
    assert response.status_code == 201, response.json()


@pytest.mark.asyncio
async def test_find_all(client: AsyncClient, create_user: ResponseDo):
    models_test = [(await create_user.do()).model, (await create_user.do()).model]
    response = await client.get(url="/users/")

    assert response.status_code == 200, response.json()

    models = [User.model_validate(user) for user in response.json()]

    assert {m.id for m in models} >= {m.id for m in models_test}, response.json()


@pytest.mark.asyncio
async def test_find_by_id(client: AsyncClient, create_user: ResponseDo):
    _id = create_user.response.json()["_id"]
    response = await client.get(url=f"/users/{_id}")
    assert response.status_code == 200, response.json()


@pytest.mark.asyncio
async def test_update(client: AsyncClient, create_user: ResponseDo):
    _id = (await create_user.do()).model.id
    response = await client.patch(
        url=f"/users/{_id}",
        content="""
                {
                   "username": "124",
                   "full_name": "124"
                }
                """,
    )
    assert response.status_code == 200, response.json()
    model = User.model_validate(response.json())
    assert model.username == "124" and model.full_name == "124", response.json()


@pytest.mark.asyncio
async def test_delete(client: AsyncClient, create_user: ResponseDo):
    _id = (await create_user.do()).model.id
    response = await client.delete(url=f"/users/{_id}")
    assert response.status_code == 200, response.json()
