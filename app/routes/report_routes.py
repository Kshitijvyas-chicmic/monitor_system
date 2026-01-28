from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.role_core import require_roles
from app.schemas.report_schema import (
    TaskPerStatusReport,
   TaskPerUserReport,
    WorkloadReport
)
from app.services.reporting_services import (
    get_tasks_per_user,
    get_tasks_per_status,
    get_workload_distribution
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/tasks-per-user",
    response_model=List[TaskPerUserReport]
)
def tasks_per_user(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "manager"]))
):
    return get_tasks_per_user(db)


@router.get(
    "/tasks-per-status",
    response_model=List[TaskPerStatusReport]
)
def tasks_per_status(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "manager"]))
):
    return get_tasks_per_status(db)


@router.get(
    "/workload",
    response_model=List[WorkloadReport]
)
def workload_distribution(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "manager"]))
):
    return get_workload_distribution(db)
