import gevent
import pytest
from httpx import AsyncClient
from locust.env import Environment

from tests.system.load.post_events.locustfile import PostEventUser


@pytest.mark.load
def test_load_test_get_near_post_event(client: AsyncClient):
    env = Environment(user_classes=[PostEventUser])
    env.create_local_runner()

    env.runner.start(100000, spawn_rate=10000)
    gevent.spawn_later(120, lambda: env.runner.quit())

    env.runner.greenlet.join()

    print('\n\n')
    print(env.stats.serialize_stats())
    print('\n')
    print(f'fails per second: {env.runner.stats.total.total_fail_per_sec}' )
    print(f'responses per second: {env.runner.stats.total.total_rps}' )
    print(f'requests count: {env.runner.stats.total.num_requests}' )
    print(f'median response time: {env.runner.stats.total.median_response_time}' )
    print(f'avg response time: {env.runner.stats.total.avg_response_time}' )

    assert env.runner.stats.total.total_fail_per_sec <= 50
    assert env.runner.stats.total.total_rps >= 1000