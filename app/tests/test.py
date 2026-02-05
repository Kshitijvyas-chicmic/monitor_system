from fastapi import FastAPI, BackgroundTasks
from app.services.notification_services import send_task_assignment_email

app = FastAPI()

@app.post("/test-email")
def test_email(background_tasks: BackgroundTasks):
    # Dummy task object
    class Task:
        title = "Test Task"
        description = "This is a test"
        priority = "High"
        due_date = "2026-01-28"
        status = "pending"

    task = Task()
    user_email = "YOUR_EMAIL@gmail.com"  # your email for testing

    # Call the background email function
    send_task_assignment_email(task, user_email, background_tasks)

    return {"message": "Email scheduled in background"}
