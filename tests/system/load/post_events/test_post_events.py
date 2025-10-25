import gevent
import pytest
from locust.env import Environment

from tests.system.load.post_events.locustfile import PostEventUser


@pytest.mark.load
def test_load_test_get_near_post_event():
    # proc = subprocess.Popen(
    #     ["python", '-m', "src.main"],
    #     stderr=subprocess.STDOUT,
    # )
    #
    # try:
    #     for _ in range(5):
    #         try:
    #             requests.get(settings.make_url(), timeout=1)
    #             break
    #         except requests.ConnectionError:
    #             time.sleep(0.5)
    #     else:
    #         pytest.fail(f"The service did not rise.")

    env = Environment(user_classes=[PostEventUser])
    env.create_local_runner()

    env.runner.start(10000, spawn_rate=1000)
    gevent.spawn_later(10, lambda: env.runner.quit())

    env.runner.greenlet.join()

    print(env.stats.serialize_stats())

    assert env.runner.stats.num_failures == 0
    assert env.runner.stats.total.total_rps >= 1000

    # finally:
    #     proc.terminate()
    #     proc.wait()
