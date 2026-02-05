# app/routes/activity_routes.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.activity_schema import ActivityLogResponse
from app.services.activity_services import get_activities_for_user, get_all_tasks,get_activities_for_task
from app.models.user import User
from app.core.role_core import require_roles
from app.core.rate_limiter import limiter


router = APIRouter(prefix="/activities", tags=["Activity Logs"])

@router.get("/",response_model=List[ActivityLogResponse])
@limiter.limit("10/minute")
def fetch_all_logs(request:Request,db:Session= Depends(get_db),current_user :User= Depends(require_roles(["admin"]))):
    return get_all_tasks(db)

@router.get("/task/{task_id}",response_model=List[ActivityLogResponse])
@limiter.limit("15/minute")
def fetch_task_activity_logs(request:Request,task_id:int, db:Session = Depends(get_db),current_user:User= Depends(require_roles(["admin","manager"]))):
    return get_activities_for_task(db, task_id)


@router.get("/user/{user_id}",response_model=List[ActivityLogResponse])
@limiter.limit("10/minute")
def fetch_all_user_activity(request:Request,user_id:int, db:Session= Depends(get_db),current_user:User = Depends(require_roles(["admin"]))):
    return get_activities_for_user(db, user_id)