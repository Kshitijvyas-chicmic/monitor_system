from fastapi import APIRouter, Depends, HTTPException, Query, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.rate_limiter import limiter
from typing import List, Optional
from app.db.session import get_db
from app.services.task import (
    create_task, get_all_tasks, get_task_by_id,
    get_users_task, update_task, update_status,
    reassign_task, delete_task, get_filtered_task
)
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskStatus, TaskResponse
from app.core.jwt import get_current_user
from app.models.user import User
from app.core.role_core import require_roles

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# only admin or manager can post the task 
@router.post("/",response_model=TaskResponse)
@limiter.limit("5/minute")
def post_task(request: Request, data:TaskCreate, background_tasks: BackgroundTasks, db:Session = Depends(get_db),
              current_user: User = Depends(require_roles(["admin","manager"]))):
    
    task = create_task(db, data, current_user.id, background_tasks)
    return task

# only admin and manager 
@router.get("/",response_model=List[TaskResponse])
@limiter.limit("10/minute")
def fetch_all_task(request: Request, db:Session =Depends(get_db), current_user:User= Depends(require_roles(["admin","manager"]))):
    return get_all_tasks(db)

# get my task all can access
@router.get("/my",response_model=List[TaskResponse])
@limiter.limit("20/minute")
def fetch_my_tasks(request: Request, db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return get_users_task(db, current_user.id)

# filter only admin and manager
@router.get("/filter",response_model=dict)
@limiter.limit("10/minute")
def filter_tasks(
    request: Request,
    status:Optional[str]= None,
    priority:Optional[str]= None,
    assigned_to_id: Optional[int] = None,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user:User=Depends(require_roles(["admin","manager"]))
):
    return get_filtered_task(db, status= status, priority=priority,assigned_to_id=assigned_to_id, sort_by=sort_by, order=order, page=page, page_size=page_size)

# get single task only admin and manager     # 
@router.get("/{task_id}", response_model = TaskResponse)
@limiter.limit("20/minute")
def fetch_task(request: Request, task_id :int, db:Session=Depends(get_db),
               current_user:User= Depends(get_current_user)):
     task = get_task_by_id(db, task_id)
     if current_user.role not in ["admin", "manager"] and task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )
     return task

# update task only admin and manager
@router.put("/{task_id}", response_model=TaskResponse)
@limiter.limit("10/minute")
def update_task_route(request: Request, task_id: int, data: TaskUpdate, db: Session = Depends(get_db),
                      current_user: User = Depends(require_roles(["admin", "manager"]))):
    task = update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# update task status - assigned user or admin/manager
@router.put("/{task_id}/status", response_model=TaskResponse)
@limiter.limit("15/minute")
def update_task_status(request: Request, task_id: int, status_data: TaskStatus, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    # Get the task first to check permissions
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if current_user.role not in ["admin", "manager"] and task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task status"
        )

    updated_task = update_status(db, task_id, status_data.status)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# reassign task only admin and manager
@router.put("/{task_id}/reassign", response_model=TaskResponse)
@limiter.limit("5/minute")
def reassign_task_route(request: Request, task_id: int, data: dict, db: Session = Depends(get_db),
                        current_user: User = Depends(require_roles(["admin", "manager"]))):
    assigned_to_id = data.get("assigned_to_id")
    if not assigned_to_id:
        raise HTTPException(status_code=400, detail="assigned_to_id is required")
    
    task = reassign_task(db, task_id, assigned_to_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or user not found")
    return task

# delete task only admin and manager
@router.delete("/{task_id}")
@limiter.limit("5/minute")
def delete_task_route(request: Request, task_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(require_roles(["admin", "manager"]))):
    # Check if task exists first
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    delete_task(db, task_id)
    return {"message": "Task deleted successfully"}
