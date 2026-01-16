from app.db.session import SessionLocal, engine
from app.models.user import User
from app.db.session import Base

# 1. Tables create karna (agar pehli baar run kar rahe ho)
Base.metadata.create_all(bind=engine)

# 2. Session create karo
db = SessionLocal()

# 3. Test user create karo
new_user = User(
    email="test@example.com",
    name="Test User",
    password="hashedpassword"
)

db.add(new_user)
db.commit()
db.refresh(new_user)

print("User created:", new_user.id, new_user.email)

# 4. Fetch user
user = db.query(User).filter(User.email == "test@example.com").first()
print("Fetched User:", user.id, user.email)

db.close()
