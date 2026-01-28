from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.schemas.task_schema import TaskCreate,TaskUpdate, TaskStatus
from app.models.user import User
from datetime import datetime
from app.services.activity_services import log_activity
from typing import Optional
from app.services.notification_services import send_task_assignment_email
from fastapi import BackgroundTasks
from app.core.config_logging import logger
# Constants
DEFAULT_STATUS = "pending"
DEFAULT_PRIORITY = "medium"
ALLOWED_SORT_FIELDS = {"created_at", "title", "priority", "status", "due_date"}
MAX_PAGE_SIZE = 100

# POST /tasks	Task create
def create_task(db:Session, data:TaskCreate, current_user:int, background_tasks: BackgroundTasks)->Task:
    logger.info("Create task request", extra={"title": data.title, "assigned_to_email": data.assigned_to_email, "created_by": current_user})
   
    if not data.title:
        logger.warning("Task creation failed - missing title", extra={"created_by": current_user})
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="task title is required")
    
    if not data.assigned_to_email:
        logger.warning("Task creation failed - missing assigned user email", extra={"created_by": current_user})
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="assigned user email is required")
    
    assigned_user = db.query(User).filter(User.email == data.assigned_to_email).first()
    if not assigned_user:
        logger.warning("Task creation failed - assigned user not found", extra={"assigned_to_email": data.assigned_to_email})
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="assigned user not found")

    new_task= Task(
        title= data.title,
        description= data.description,
        assigned_to_id= assigned_user.id,
        created_by_id =current_user,
        status= data.status or DEFAULT_STATUS,
        priority=data.priority or DEFAULT_PRIORITY,
        due_date= data.due_date,
        created_at = datetime.utcnow()
    )
   
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    logger.info("Task created successfully", extra={"task_id": new_task.id, "assigned_to": assigned_user.id})

    log_activity(
        db=db,
        actor_id=current_user,
        action="TASK_CREATED",
        entity_type="TASK",
        entity_id=new_task.id,
        description="New task created"
    )
    
    # send_task_assignment_email(new_task, assigned_user.email, background_tasks)
    logger.info("Task assignment email triggered", extra={"task_id": new_task.id, "assigned_to": assigned_user.email})
    return new_task
    
    
# GET /tasks	All tasks
def get_all_tasks(db:Session):
    tasks = db.query(Task).all()
    logger.info("Fetched all tasks", extra={"count": len(tasks)})
    return tasks
    
# GET /tasks/my	Logged-in user task
def get_users_task(db:Session, assigned_to_id:int):
    tasks = db.query(Task).filter(Task.assigned_to_id == assigned_to_id).all()
    logger.info("Fetched tasks for user", extra={"user_id": assigned_to_id, "count": len(tasks)})
    return tasks


def get_task_by_id(db:Session, task_id:int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Task not found", extra={"task_id": task_id})
        raise HTTPException(status_code=404, detail=f"Task not found for id {task_id}")
    logger.info("Task retrieved", extra={"task_id": task.id})
    return task
    

def update_task(db:Session, data:TaskUpdate, task_id:int, current_user):
  
        task = get_task_by_id(db,task_id)
        if not task:
             raise HTTPException(status_code=404,detail=f"task not found for id")
        
        update_data = data.dict(exclude_unset=True)

# setattr(object, attribute_name, value)
        for key, value  in update_data.items():
            setattr(task,key, value)

        db.commit()
        db.refresh(task)
        logger.info("Task updated successfully", extra={"task_id": task.id, "updated_by": current_user.id})

        log_activity(
        db=db,
        actor_id=current_user.id,
        action="TASK_UPDATED",
        entity_type="TASK",
        entity_id=task.id,
        description="Task is updated by admin"
    )
        return task
    
    
def update_status(db:Session, task_id:int , new_status:TaskStatus, current_user:User):
    
        task = get_task_by_id(db, task_id)
        if current_user.role == "employee":
            if task.assigned_to_id != current_user.id:
                logger.warning("Employee trying to update unassigned task", extra={"task_id": task.id, "user_id": current_user.id})
                raise HTTPException(403, "You can update only your assigned task")
        if not task:
         raise HTTPException(status_code=404,detail=f"task not found for id")
    
        task.status = new_status.value

        db.commit()
        db.refresh(task)
        logger.info("Task status updated", extra={"task_id": task.id, "status": new_status.value, "updated_by": current_user.id})

        log_activity(
        db=db,
        actor_id=current_user.id,
        action="STATUS_UPDATED",
        entity_type="TASK",
        entity_id=task.id,
        description="Task status is updated by user"
    )

        return task


def reassign_task(db:Session,  task_id:int,new_user_id:int,current_user_id:int ):
       
            task= get_task_by_id(db, task_id)
            if not task:
                logger.warning("Task reassignment failed - new user not found", extra={"task_id": task.id, "new_user_id": new_user_id})
                raise HTTPException(status_code=404, detail="Task not found")
            
            new_user = db.query(User).filter(User.id == new_user_id).first()
            if not new_user:
                raise HTTPException(status_code=404, detail="user not found")
            
            if task.assigned_to_id == new_user_id:
                raise HTTPException(
            status_code=400,
            detail="Task is already assigned to this user"
        )
            if task.status == "completed":
                  raise HTTPException(
            status_code=400,
            detail="Completed task cannot be reassigned"
        )
            
            old_assignee = task.assigned_to_id
            task.assigned_to_id = new_user_id

            db.commit()
            db.refresh(task)
            log_activity(
                db=db,
                actor_id=current_user_id,
                action="TASK_REASSIGNED",
                entity_type="TASK",
                entity_id=task.id,
                description=f"Task reassigned from user {old_assignee} to {new_user_id}"
            )
            return task


# DELETE /tasks/{id}	Delete
def delete_task(db:Session, task_id:int, current_user:User):
  
        task= get_task_by_id(db,task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        logger.info("Task deleted successfully", extra={"task_id": task.id, "deleted_by": current_user.id})

        log_activity(
        db=db,
        actor_id=current_user.id,
        action="TASK_DELETED",
        entity_type="TASK",
        entity_id=task.id,
        description=f"Task IS deleted by {current_user.name}"
        )
        return {"message":"task deleted successfully"}


# GET /tasks?filters	Filtering

def get_filtered_task(db:Session,
                      status:Optional[str]=None,
                      priority:Optional[str]=None,
                      assigned_to_id:Optional[int]=None,
                      sort_by:str ="created_at",
                      order:str="desc",
                      page:int=1,
                      page_size:int=10):
    query = db.query(Task)
    # filter
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assigned_to_id:
        query = query.filter(Task.assigned_to_id == assigned_to_id)

    # sorting
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    sort_column = getattr(Task, sort_by)
    query = query.order_by(
        sort_column.asc() if order == "asc" else sort_column.desc()
    )

    # pagination
    if page_size > MAX_PAGE_SIZE:
        page_size = MAX_PAGE_SIZE
    offset = (page - 1) * page_size
    total = query.count()
    tasks = query.offset(offset).limit(page_size).all()
    logger.info("Filtered tasks fetched", extra={"count": len(tasks), "page": page, "page_size": page_size})
    
    # Convert tasks to dicts
    task_dicts = []
    for task in tasks:
        task_dicts.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "assigned_to_id": task.assigned_to_id,
            "created_by_id": task.created_by_id,
            "created_at": task.created_at,
            "due_date": task.due_date
        })
    
    return {
        "tasks": task_dicts,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

