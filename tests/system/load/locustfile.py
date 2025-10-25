from locust import HttpUser, between

from tests.system.load.utils.tasks_loader import load_loading_tests


class ServiceUser(HttpUser):
    wait_time = between(1, 3)

    tasks = load_loading_tests('tests.system.load.tasks')
