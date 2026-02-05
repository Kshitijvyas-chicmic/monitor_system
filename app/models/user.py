from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)  
    provider = Column(String, default="local")  
    provider_id = Column(String, nullable=True) 
    is_verified = Column(Boolean, default=False)
    role = Column(String,ForeignKey("roles.id"),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)