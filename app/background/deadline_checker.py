from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.services.notification_services import send_task_overdue_email
from fastapi import BackgroundTasks
from app.services.activity_services import log_activity

def check_deadlines(db:Session, background_tasks:BackgroundTasks):
    now  = datetime.utcnow()
    email = db.query(Task).filter(Task.assigned_to_id.isnot(None)).first()
    overdue_tasks = db.query(Task).filter(Task.due_date < now , Task.status != "completed").all()

    for task in overdue_tasks:
        task.priority ="high"
        log_activity(
            db=db,
            actor_id= task.created_by_id,
            action="TASK_OVERDUE",
            entity_type="TASK",
            entity_id= task.id,
            description="task automatically marked as overdue"
        )
        send_task_overdue_email(task, email, background_tasks)


    db.commit()