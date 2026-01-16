
from app.db.session import engine, Base

# 👇 THIS IS THE KEY LINE (MOST IMPORTANT)
from app.models.user import User  

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully")




