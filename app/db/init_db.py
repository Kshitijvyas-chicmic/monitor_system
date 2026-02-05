
from app.db.session import engine, Base

# 👇 THIS IS THE KEY LINE (MOST IMPORTANT)
from app.models.user import User  
from app.models.task_db import Task
from app.models.role_db import Role
from app.models.comment_model import Comment
from app.models.activity_model import ActivityLog
print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")




