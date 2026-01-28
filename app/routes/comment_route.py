from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.jwt import get_current_user
from app.schemas.comment_schema import CommentCreate, CommentResponse, CommentUpdate
from app.services.comment_service import (
    create_comment,
    get_comment_by_task,
      update_comment, delete_comment
)
from app.models.user import User
from app.core.rate_limiter import limiter


router = APIRouter(
    prefix="/tasks/{task_id}/comments",
    tags=["Comments"]
)


@router.post("/",response_model=CommentResponse)
@limiter.limit("10/minute")
def add_comment(
    request:Request,
    task_id:int,
    data:CommentCreate,
    db:Session=Depends(get_db),
    current_user :User= Depends(get_current_user)
):
    return create_comment(
        db=db,
        task_id=task_id,
        data= data.content,
        current_user=current_user
    )

@router.get("/",response_model=List[CommentResponse])
@limiter.limit("30/minute")
def list_comments(
    request:Request,
    task_id:int,
    db:Session= Depends(get_db),
):
    return get_comment_by_task(db, task_id)

@router.put("/{comment_id}", response_model=CommentResponse)
@limiter.limit("10/minute")
def edit_comment(
    request:Request,
    task_id: int,
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_comment(db, comment_id, data, task_id, current_user)


@router.delete("/{comment_id}")
@limiter.limit("5/minute")
def remove_comment(
    request:Request,
    task_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_comment(db, comment_id,task_id, current_user)
