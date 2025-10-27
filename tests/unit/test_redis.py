import pytest
import redis
from httpx import AsyncClient
from redis import Redis

from src.models.post_event import SquareNearPostEvents
from src.services.post_event import find_near_post_events


@pytest.mark.asyncio
async def test_redis(client: AsyncClient):
    print("\n\n")

    l1 = (37.6173, 55.7558)
    pe1 = await find_near_post_events(l1)
    r1 = SquareNearPostEvents(
        post_events=pe1
    ).model_dump_json()
    l2 = (54.6173, 56.7558)
    pe2 = await find_near_post_events(l2)
    r2 = SquareNearPostEvents(
        post_events=pe2
    ).model_dump_json()
    l3 = (68.6173, 60.7558)
    pe3 = await find_near_post_events(l3)
    r3 = SquareNearPostEvents(
        post_events=pe3
    ).model_dump_json()

    l4 = (54, 56)

    r: Redis = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    # await r.delete("post_events:*")
    r.geoadd("post_events", l1 + (r1,))
    r.geoadd("post_events", l2 + (r2,))
    r.geoadd("post_events", l3 + (r3,))

    near_post_events = r.geosearch(
        "post_events",
        longitude=l4[0],
        latitude=l4[1],
        unit="km",
        width=200,
        height=200,
        sort="ASC",
        count=1,
    )

    post_event = None
    if len(near_post_events) == 1:
        post_event = SquareNearPostEvents.model_validate_json(near_post_events[0])

    print(post_event.post_events[0].id)

    r.close()
