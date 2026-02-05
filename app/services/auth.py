from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.schema import UserCreate , UserUpadte
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.services.activity_services import log_activity

def sign_up(db:Session, user:UserCreate):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= 400,detail = "user already exist")
    
    new_user = User(
         name=user.name,
        email = user.email,
        password=hash_password(user.password),
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_activity(
        db=db,
        actor_id=new_user.id,
        action="USER_CREATED",
        entity_type="USER",
        entity_id=new_user.id,
        description="New user registered"
    )
    return new_user

def login(db:Session, email:str, password:str):
    user = db.query(User).filter(User.email==email).first()

    if not user or not verify_password(password , user.password):
        raise HTTPException(status_code= 401, detail="invalid credentials")
    
    token = create_access_token({"sub":str(user.id)
                  ,  "role": user.role  })
       

    return {
        "access_token": token,
        "token_type":"bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
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
    log_activity(
        db=db,
        actor_id=user_id,
        action="USER_UPDATED",
        entity_type="USER",
        entity_id=user_id,
        description="user update profile"
    )
    return user

def delete_user(db:Session, user_id:int , current_user:User):
    user = get_user_by_id(db , user_id)
    
    # Delete all activity logs for this user
    from app.models.activity_model import ActivityLog
    db.query(ActivityLog).filter(ActivityLog.actor_id == user_id).delete()
    
    db.delete(user)
    db.commit()
    log_activity(
        db=db,
        actor_id=current_user.id,
        action="USER_DELETED",
        entity_type="USER",
        entity_id=user.id,
        description="user deleted by admin"
    )
    return {"message":"user deleted successfully"}    
    

def change_password(db:Session , user_id:int, old_password:str, new_password:str):
    user = get_user_by_id(db,user_id)
    if not user or not verify_password(old_password, user.password):
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    user.password= hash_password(new_password)
    db.commit()
    db.refresh(user)
    log_activity(
        db=db,
        actor_id=user.id,
        action="PASSWORD_CREATED",
        entity_type="USER",
        entity_id=user.id,
        description="Password changed by user"
    )
    return {"message":"password updated successfully"}

def role_change(db:Session,admin_id:int, user_id:int, new_role:str):
    admin = get_user_by_id(db, admin_id)
    if admin.role != "admin":
        raise HTTPException(403,"only admin can change the role")
    
    if new_role not in ["employee","admin","manager"]:
        raise HTTPException(400," invalid role")
    
    user= get_user_by_id(db,user_id)
    user.role= new_role
    db.commit()
    db.refresh(user)

    log_activity(
        db=db,
        actor_id=admin.id,
        action="ROLE_UPDATED",
        entity_type="USER",
        entity_id=user.id,
        description="user's role updated"
    )
    return user
         

