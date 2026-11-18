from locust import HttpUser, between, task


class OrderUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def create_order(self):
        self.client.post(
            "/orders",
            json={"user_id": 1, "product_id": 2, "quantity": 1},
        )
