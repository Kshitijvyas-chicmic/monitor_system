from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.task_db import Task
from app.models.user import User

def get_tasks_per_user(db:Session):
    return (
        db.query(User.id.label("user_id"),
                 User.email,
                 func.count(Task.id).label("total_tasks"))
                 .join(Task, Task.assigned_to_id == User.id).group_by(User.id).all())


def get_tasks_per_status(db:Session):
    return (
        db.query(Task.status,
                 func.count(Task.id).label("total_tasks"))
                 .group_by(Task.status).all())


def get_workload_distribution(db:Session):
    return(
        db.query(
            User.id.label("user_id"),
            User.email,
            func.count(case((Task.status !="in_progress",1))).label("open_tasks"),
            func.count(case((Task.status == "completed",1))).label("completed_tasks")
        )
        .join(Task, Task.assigned_to_id == User.id).group_by(User.id).all()
    )