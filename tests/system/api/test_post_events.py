import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.models.post_event import PostEvent
from src.utils.tests.other import output_response
from src.utils.tests.response_models import ResponseDo, ResponseModel
from tests.system.api.test_promotions import create_promotion  # noqa: F401
from tests.system.api.test_users import create_user  # noqa: F401


@pytest_asyncio.fixture
async def create_post_event(client: AsyncClient, create_user: ResponseDo) -> ResponseDo:
    async def _create_post_event() -> ResponseModel:
        user_id = str(create_user.model.id)
        response = await client.post(
            url="/post-events/",
            content="""
                    {
                      "name": "Dance party",
                      "description": "We are gathering close to the center. Let's dance and have fun!",
                      "author": \"""" + user_id + """\",
                      "images": [
                        {
                          "url": "string",
                          "description": "string"
                        }
                      ],
                      "location": {
                        "type": "Point",
                        "coordinates": [
                          46.459305,
                          30.752031
                        ]
                      }
                    }
                    """,
        )
        assert response.status_code == 201, output_response(response)
        model = PostEvent(**response.json())
        return ResponseModel(response=response, model=model)

    post_event = await _create_post_event()
    return ResponseDo(
        response=post_event.response, model=post_event.model, do=_create_post_event
    )


@pytest.mark.asyncio
async def test_create(client: AsyncClient, create_post_event: ResponseDo):
    response = create_post_event.response
    assert response.status_code == 201, response.json()


@pytest.mark.asyncio
async def test_find_near(client: AsyncClient, create_post_event: ResponseDo):
    models_test = [
        (await create_post_event.do()).model,
        (await create_post_event.do()).model,
    ]
    response = await client.get(url="/post-events/?longitude=37.6173&latitude=55.7558")

    assert response.status_code == 200, response.json()

    models = [PostEvent.model_validate(post_event) for post_event in response.json()]

    assert {m.id for m in models} >= {m.id for m in models_test}, response.json()


@pytest.mark.asyncio
async def test_add_promotion(
    client: AsyncClient, create_post_event: ResponseDo, create_promotion: ResponseDo
):
    models_test = [
        (await create_post_event.do()).model,
        (await create_post_event.do()).model,
    ]
    promotion = (await create_promotion.do()).model
    response = await client.get(
        url=f"/post-events/{models_test[1].id}/add-promotion/{promotion.id}"
    )

    assert response.status_code == 200, response.json()

    models_test[1] = PostEvent.model_validate(response.json())

    response = await client.get(url="/post-events/?longitude=37.6173&latitude=55.7558")
    models = [PostEvent.model_validate(post_event) for post_event in response.json()]
    models_promotions = [
        m.promotions
        for i, m in enumerate(models)
        if m.id in {mt.id for mt in models_test}
    ]

    assert not models_promotions[1] and models_promotions[0], response.json()


@pytest.mark.asyncio
async def test_find_by_id(client: AsyncClient, create_post_event: ResponseDo):
    _id = create_post_event.response.json()["_id"]
    response = await client.get(url=f"/post-events/{_id}")
    assert response.status_code == 200, response.json()


@pytest.mark.asyncio
async def test_update(client: AsyncClient, create_post_event: ResponseDo):
    _id = (await create_post_event.do()).model.id
    response = await client.patch(
        url=f"/post-events/{_id}",
        content="""
                {
                    "description": "We are the close"
                }
                """,
    )
    assert response.status_code == 200, response.json()
    model = PostEvent.model_validate(response.json())
    assert model.updated_at is not None and model.created_at is not None, (
        response.json()
    )


@pytest.mark.asyncio
async def test_delete(client: AsyncClient, create_post_event: ResponseDo):
    _id = (await create_post_event.do()).model.id
    response = await client.delete(url=f"/post-events/{_id}")
    assert response.status_code == 200, response.json()
