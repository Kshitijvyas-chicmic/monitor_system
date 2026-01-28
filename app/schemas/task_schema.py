from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from enum import Enum


class TaskBase(BaseModel):
    title:str
    description:Optional[str]=None
    priority:str="medium"
    due_date:Optional[date]= None

class TaskCreate(TaskBase):
    assigned_to_email: str
    status: str = "pending"


class TaskUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None
    priority:Optional[str]=None
    due_date:Optional[date]=None

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"


class TaskResponse(TaskBase):
    id:int
    status:str
    assigned_to_id:int
    created_by_id:int
    created_at:datetime
    
    class Config:
         from_attributes = True

