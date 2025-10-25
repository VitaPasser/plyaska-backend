from locust import TaskSet, task

class PostEventTasks(TaskSet):
    @task
    def get_near_post_event(self):
        self.client.get("/post-events/?longitude=37.6173&latitude=55.7558")
