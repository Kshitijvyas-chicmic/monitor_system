from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)  # TASK / COMMENT / USER
    entity_id = Column(Integer, nullable=False)

    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
