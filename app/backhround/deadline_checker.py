from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.services.activity_services import log_activity

def check_deadlines(db:Session):
    now  = datetime.utcnow()

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

    db.commit()