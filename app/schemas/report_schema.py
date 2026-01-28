from pydantic import BaseModel
from typing import List

class TaskPerUserReport(BaseModel):
    user_id:int
    email:str
    total_tasks:int

class TaskPerStatusReport(BaseModel):
    status:str
    total_tasks:int

class WorkloadReport(BaseModel):
    user_id:int
    email:str
    open_tasks:int
    completed_tasks:int