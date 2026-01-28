from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.comment_model import Comment
from app.models.task_db import Task
from app.models.user import User
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.services.activity_services import log_activity
def create_comment(
        db:Session,
        task_id:int,
        data:CommentCreate,
        current_user:User
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tas not found"
        )
    
    if current_user.role =="employee":
        if task.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="you can comment on your task only"
            )
        
    comment= Comment(
        content= data,
        task_id=task_id,
        user_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    log_activity(
    db=db,
    actor_id=current_user.id,
    action="COMMENT_CREATED",
    entity_type="TASK",
    entity_id=task_id,
    description=f"Comment added to task {task_id}"
)
    return comment

def get_comment_by_task(
        db:Session,
        task_id:int
):
    comment=  db.query(Comment).filter(Comment.task_id==task_id).order_by(Comment.created_at.asc()).all()
    return comment


def update_comment(db: Session, comment_id: int, data: CommentUpdate,task_id:int, user: User):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = data.content
    db.commit()
    db.refresh(comment)
    log_activity(
    db=db,
    actor_id=user.id,
    action="COMMENT_UPDATED",
    entity_type="TASK",
    entity_id=task_id,
    description=f"Comment added to task {task_id}"
)
    return comment


def delete_comment(db: Session, comment_id: int,task_id:int, user: User):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    db.delete(comment)
    db.commit()
    log_activity(
    db=db,
    actor_id=user.id,
    action="COMMENT_CREATED",
    entity_type="TASK",
    entity_id=task_id,
    description=f"Comment added to task {task_id}"
)
    return {"message": "Comment deleted successfully"}
