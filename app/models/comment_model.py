from sqlalchemy import Column,Integer,String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Comment(Base):
    __tablename__="comments"

    id = Column(Integer, primary_key =True,index=True)
    content = Column(String, nullable=False)

    task_id= Column(Integer, ForeignKey("tasks.id"),nullable=False)
    user_id= Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
