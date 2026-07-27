from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self) -> None:
        self.client.get("/")
