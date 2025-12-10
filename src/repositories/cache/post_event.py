import pickle
from typing import Tuple

from src.main import main
from src.models.post_event import PostEvent, PostEventNear, SquareNearPostEvents


async def find_near_post_events_square(
    coordinates: Tuple[float, float],
) -> list[PostEventNear]:
    r = await main.get_connect_cache()
    near_post_events: list[bytes] = await r.geosearch(
        PostEventNear.get_like_db_name(),
        longitude=coordinates[0],
        latitude=coordinates[1],
        unit="m",
        width=250,
        height=250,
        sort="ASC",
        count=1,
    )

    if len(near_post_events) == 0:
        return []

    square: SquareNearPostEvents = pickle.loads(near_post_events[0])
    return square.post_events


async def add_post_events_in_square(
    coordinates: Tuple[float, float], post_events: list[PostEventNear]
):
    r = await main.get_connect_cache()
    square = SquareNearPostEvents(post_events=post_events)
    square_bytes = pickle.dumps(square)
    await r.geoadd(PostEventNear.get_like_db_name(), coordinates + (square_bytes,))


async def delete_post_events_square(post_event: PostEvent):
    r = await main.get_connect_cache()

    near_post_events: list[bytes] = await r.geosearch(
        PostEventNear.get_like_db_name(),
        longitude=post_event.location.coordinates[0],
        latitude=post_event.location.coordinates[1],
        unit="m",
        width=250,
        height=250,
        sort="ASC",
    )

    if len(near_post_events) == 0:
        return

    await r.zrem(PostEventNear.get_like_db_name(), *near_post_events)
