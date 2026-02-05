from pydantic import BaseModel
from datetime import datetime

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
    updated_At:datetime

    class config:
        from_attributes=True