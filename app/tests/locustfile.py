from locust import HttpUser, task, between
import random

class CommentUser(HttpUser):
    wait_time = between(2, 5)  # realistic delay
    token = None
    task_ids = [1, 2, 3]   # existing task IDs
    comment_ids = []

    def on_start(self):
        """
        Login once per user
        """
        response = self.client.post(
            "/login",
            json={
                "email": "employee@test.com",
                "password": "password123"
            }
        )

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

    @task(3)
    def create_comment(self):
        """
        CREATE comment
        """
        task_id = random.choice(self.task_ids)

        response = self.client.post(
            f"/tasks/{task_id}/comments",
            json={
                "content": "This is a locust test comment"
            },
            name="POST /tasks/:id/comments"
        )

        if response.status_code == 200:
            self.comment_ids.append(response.json()["id"])

    @task(2)
    def get_comments(self):
        """
        GET comments by task
        """
        task_id = random.choice(self.task_ids)

        self.client.get(
            f"/tasks/{task_id}/comments",
            name="GET /tasks/:id/comments"
        )

    @task(1)
    def update_comment(self):
        """
        UPDATE comment
        """
        if not self.comment_ids:
            return

        comment_id = random.choice(self.comment_ids)
        task_id = random.choice(self.task_ids)

        self.client.put(
            f"/tasks/{task_id}/comments/{comment_id}",
            json={
                "content": "Updated by locust"
            },
            name="PUT /tasks/:id/comments/:id"
        )

    @task(1)
    def delete_comment(self):
        """
        DELETE comment
        """
        if not self.comment_ids:
            return

        comment_id = self.comment_ids.pop()
        task_id = random.choice(self.task_ids)

        self.client.delete(
            f"/tasks/{task_id}/comments/{comment_id}",
            name="DELETE /tasks/:id/comments/:id"
        )
