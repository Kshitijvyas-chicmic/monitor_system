from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class CommentCreate(BaseModel):
    content:str

class CommentUpdate(BaseModel):
    content:str

class CommentResponse(BaseModel):
    id:int
    content:str
    task_id:int
    user_id:int
    created_at:datetime
    updated_at: Optional[datetime] 
    class config:
        from_attributes=True