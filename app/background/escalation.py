from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.services.notification_services import send_task_escalation_email
from fastapi import BackgroundTasks


def esclate_tasks(db:Session, background_tasks:BackgroundTasks):
    thrushold= datetime.utcnow() - timedelta(days=2)
    email = db.query(Task).filter(Task.assigned_to_id.isnot(None)).first()
    tasks= db.query(Task).filter(
        Task.due_date < thrushold, Task.status!= "completed"
    ).all()

    for task in tasks:
        task.status = "blocked"
        send_task_escalation_email(task, email, background_tasks)
    

    db.commit()