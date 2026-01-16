from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.schema import UserCreate

def sign_up(db:Session, user:UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= 400,detail = "user already exist")
    
    new_user = User(
         name=user.name,
        email = user.email,
        password= user.password,
        role = "employee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(db:Session, email:str, password:str):
    user = db.query(User).filter(User.email==email).first()
    if not user or user.password != password:
        raise HTTPException(status_code= 401, detail="invalid credentials")
    return user

