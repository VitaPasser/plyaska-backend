from locust import TaskSet, task

class PostEventTasks(TaskSet):
    @task
    def get_near_post_event(self):
        self.client.get("/post-events/?longitude=46.45&latitude=30.75")
