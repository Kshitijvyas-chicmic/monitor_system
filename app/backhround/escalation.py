from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.task_db import Task

def esclate_tasks(db:Session):
    thrushold= datetime.utcnow() - timedelta(days=2)

    tasks= db.query(Task).filter(
        Task.due_date < thrushold, Task.status!= "completed"
    ).all()

    for task in tasks:
        task.status = "blocked"

    db.commit()