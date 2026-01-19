# POST /tasks	Task create
# GET /tasks	All tasks
# GET /tasks/{id}	Task detail
# GET /tasks/my	Logged-in user tasks
# PUT /tasks/{id}	Update task
# PATCH /tasks/{id}/status	Update status
# PATCH /tasks/{id}/assign	Reassign
# DELETE /tasks/{id}	Delete

# GET /tasks?filters	Filtering
# GET /tasks/{id}/activity	Audit log



from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.task_db import Task
from app.schemas.task_schema import TaskCreate,TaskUpdate, TaskStatus
from app.models.user import User
from datetime import datetime


# POST /tasks	Task create
def create_task(db:Session, data:TaskCreate ,current_user:int)->Task:

    if not data.title:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="task title is required")
    
    if not data.assigned_to_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="assigned user id is required")
    
    assigned_user = db.query(User).filter(User.id == data.assigned_to_id).first()
    if not assigned_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="assigned user not found")

    new_task= Task(
        title= data.title,
        description= data.description,
        assigned_to_id= data.assigned_to_id,
        created_by_id =current_user,
        status="pending",
        priority=data.priority or "medium",
        due_date= data.due_date,
        created_at = datetime.utcnow()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

# GET /tasks	All tasks
def get_all_task(db:Session):

    try:
        tasks=db.query(Task).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Internal server err:{str(e)}")
    

def get_task_by_id(db:Session, task_id:int):
    try:
        task= db.query(Task).filter(task_id ==Task.id ).first()
        if not task:
            raise HTTPException(status_code=404,detail=f"task not found for id{task_id}")
        return task
    except Exception as e:
        raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")
    
# GET /tasks/my	Logged-in user tasks


def get_users_task(db:Session, assigned_to_id:int):
    try:
        tasks= db.query(Task).filter(Task.assigned_to_id == assigned_to_id).all()
        if not tasks:
            raise HTTPException(status_code=404,detail=f"task not found for id")
        return tasks
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")

def update_task(db:Session, data:TaskUpdate, task_id:int):
    try:
        task = get_task_by_id(db,task_id)
        if not task:
             raise HTTPException(status_code=404,detail=f"task not found for id")
        
        updatetask = data.dict(exclude_unset=True)

# setattr(object, attribute_name, value)
        for key, value  in updatetask.items():
            setattr(task,key, value)

        db.commit()
        db.refresh(task)
        return task
    
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")
    
def update_status(db:Session, task_id:int , new_status:TaskStatus):
    try:
        task = get_task_by_id(db, task_id)
        if not task:
         raise HTTPException(status_code=404,detail=f"task not found for id")
    
        task.status = new_status.value

        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")



def reassign_task(db:Session,  task_id:int,new_user_id:int,current_user_id:int ):
        try:
            task= get_task_by_id(db, task_id)
            if not task:
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

            return task


        except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")



# DELETE /tasks/{id}	Delete
def delete_task(db:Session, task_id:int):
    try:
        task= get_task_by_id(db,task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return {"message":"task deleted successfully"}

    except Exception as e:
         raise HTTPException(status_code= 500, detail=f"Internal server error:{str(e)}")


