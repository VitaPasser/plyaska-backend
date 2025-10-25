from locust import HttpUser, between

from src.utils.config import settings
from tests.system.load.post_events.tasks.post_event import PostEventTasks


class PostEventUser(HttpUser):
    host = settings.make_url()
    wait_time = between(1, 3)

    tasks = [PostEventTasks]
