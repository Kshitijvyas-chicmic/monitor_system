from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.schema import UserCreate , UserUpadte
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

def sign_up(db:Session, user:UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= 400,detail = "user already exist")
    
    new_user = User(
         name=user.name,
        email = user.email,
        password=hash_password(user.password),
        role = "employee"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(db:Session, email:str, password:str):
    user = db.query(User).filter(User.email==email).first()

    if not user or not verify_password(password , user.password):
        raise HTTPException(status_code= 401, detail="invalid credentials")
    
    token = create_access_token({"sub":str(user.id)})

    return {
        "access_token": token,
        "token_type":"bearer"
    }

def get_all_user(db :Session):
    
    return db.query(User).all()

def get_user_by_id(db:Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db:Session, user_id:int, data:UserUpadte):
    user = get_user_by_id(db ,user_id)
    if data.name:
        user.name= data.name

    db.commit()
    db.refresh(user)
    return user

def delete_user(db:Session, user_id:int):
    user = get_user_by_id(db , user_id)
    db.delete(user)
    db.commit()
    return {"message":"user deleted successfully"}    
    

def change_password(db:Session , user_id:int, old_password:str, new_password:str):
    user = get_user_by_id(db,user_id)
    if not user or not verify_password(old_password, user.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    user.password= hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"message":"password updated successfully"}