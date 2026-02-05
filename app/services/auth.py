from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.schema import UserCreate , UserUpadte
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.services.activity_services import log_activity
from fastapi import BackgroundTasks
from app.services.notification_services import send_welcome_email, send_login_alert_email,send_password_change_email,send_role_change_email, send_verification_email
from app.core.config_logging import logger
from app.core.google_auth import verify_google_token
from app.models.activity_model import ActivityLog
from app.core.verification_token import generate_verification_token , save_token, verify_token
from app.core.github_auth import verify_github_code


# def sign_up(db:Session, user:UserCreate, background_tasks:BackgroundTasks):
#     logger.info("Signup request received", extra={"email": user.email})
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         logger.warning("Signup failed - user exists", extra={"email": user.email})
#         raise HTTPException(status_code= 400,detail = "user already exist")
    
#     new_user = User(
#          name=user.name,
#         email = user.email,
#         password=hash_password(user.password),
#         role = user.role,
#         is_verified = False
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     logger.info("User created successfully", extra={"user_id": new_user.id, "email": new_user.email})
#     token , expiry = generate_verification_token(length=6 , expiry = 5)
#     save_token(new_user.email, token , expiry)
#     send_verification_email(new_user.email,token, background_tasks)
#     log_activity(
#         db=db,
#         actor_id=new_user.id,
#         action="USER_CREATED",
#         entity_type="USER",
#         entity_id=new_user.id,
#         description="New user registered"
#     )
#     send_welcome_email(new_user.email, background_tasks, new_user.name)
#     return new_user
def sign_up(db: Session, user: UserCreate, background_tasks: BackgroundTasks):
    logger.info("Signup request received", extra={"email": user.email})
    
    if db.query(User).filter(User.email == user.email).first():
        logger.warning("Signup failed - user exists", extra={"email": user.email})
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        is_verified=False,
        provider="local"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Verification token
    token, expiry = generate_verification_token(length=6, expiry=5)
    save_token(new_user.email, token, expiry)
    send_verification_email(new_user.email, token, background_tasks)
    send_welcome_email(new_user.email, background_tasks, new_user.name)

    log_activity(
        db=db,
        actor_id=new_user.id,
        action="USER_CREATED",
        entity_type="USER",
        entity_id=new_user.id,
        description="New user registered"
    )
    
    return new_user

# ------------------- LOGIN ------------------- #
def login(db: Session, email: str, password: str, background_tasks: BackgroundTasks):
    logger.info("Login attempt", extra={"email": email})
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.password or not verify_password(password, user.password):
        logger.warning("Login failed - invalid credentials", extra={"email": email})
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    
    token = create_access_token({"sub": str(user.id), "role": user.role})
    send_login_alert_email(user.email, background_tasks, user.name)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    }

# ------------------- GOOGLE OAUTH LOGIN ------------------- #
def google_oauth_login(db: Session, id_token_str: str):
    """
    Option 1 approach: No password stored.
    Verifies Google ID token, creates user if not exists.
    """
    # print(id_token_str)
    # Verify Google token
    try:
        id_info = verify_google_token(id_token_str)
    except Exception as e:
        logger.warning(f"Google login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = id_info.get("email")
    name = id_info.get("name")
    provider_id = id_info.get("sub")

    if not email:
        raise HTTPException(status_code=400, detail="Google token missing email")

    # Check or create user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            password=None,         # No password for Google users
            role="employee",
            is_verified=True,
            provider="google",
            provider_id=provider_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        log_activity(
            db=db,
            actor_id=user.id,
            action="USER_CREATED",
            entity_type="USER",
            entity_id=user.id,
            description="User registered via Google"
        )

    # JWT token
    token = create_access_token({"sub": str(user.id), "role": user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    }


def github_oauth_login(db: Session, code: str):
    # 1. Verify GitHub code
    print(code)
    github_data = verify_github_code(code)
    print(github_data)
    email = github_data["email"]
    name = github_data["name"]
    provider_id = github_data["provider_id"]

    # 2. Check user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.info(f"Creating new user from GitHub login: {email}")

        user = User(
            name=name,
            email=email,
            password=None,
            role="employee",
            is_verified=True,
            provider="github",
            provider_id=provider_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        logger.info(f"GitHub login for existing user: {email}")
    
    log_activity(
            db=db,
            actor_id=user.id,
            action="USER_CREATED",
            entity_type="USER",
            entity_id=user.id,
            description="User registered via Github"
        )
    # 3. Generate JWT
    token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })
    print(token)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    }

def verify_user_email(db:Session, email:str, token:str):
    logger.info("Email verification attempt", extra={"email": email})

    if not verify_token(email,token):
        logger.warning("Email verification failed - invalid token", extra={"email": email})
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning("Email verification failed - user not found", extra={"email": email})
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    db.commit()
    db.refresh(user)
    logger.info("Email verified successfully", extra={"user_id": user.id, "email": email})
    return user

# def login(db:Session, email:str, password:str, background_tasks:BackgroundTasks):
#     logger.info("Login attempt", extra={"email": email})
#     user = db.query(User).filter(User.email==email).first()

#     if not user or not verify_password(password , user.password):
#         logger.warning("Login failed - invalid credentials", extra={"email": email})
#         raise HTTPException(status_code= 401, detail="invalid credentials")

#     if not user.is_verified:
#         logger.warning("Login failed - email not verified", extra={"email": email})
#         raise HTTPException(
#             status_code=403, 
#             detail="Email not verified. Please verify your email first."
#         )

#     token = create_access_token({"sub":str(user.id)
#                   ,  "role": user.role  })
#     logger.info("Login successful", extra={"user_id": user.id, "email": email})
#     send_login_alert_email(user.email, background_tasks, user.name)   

#     return {
#         "access_token": token,
#         "token_type":"bearer",
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "role": user.role
#         }
#     }


def get_all_user(db :Session):
    users = db.query(User).all()
    logger.info("Fetched all users", extra={"count": len(users)})
    return users


def get_user_by_id(db:Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning("User not found", extra={"user_id": user_id})
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("User retrieved", extra={"user_id": user.id, "email": user.email})
    return user


def update_user(db:Session, user_id:int, data:UserUpadte):
    user = get_user_by_id(db ,user_id)
    if data.name:
        old_name= user.name
        user.name= data.name
        logger.info("User name updated", extra={"user_id": user.id, "old_name": old_name, "new_name": data.name})


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
    

    db.query(ActivityLog).filter(ActivityLog.actor_id == user_id).delete()
    
    db.delete(user)
    db.commit()
    logger.info("User deleted", extra={"user_id": user_id, "deleted_by": current_user.id})
    log_activity(
        db=db,
        actor_id=current_user.id,
        action="USER_DELETED",
        entity_type="USER",
        entity_id=user.id,
        description="user deleted by admin"
    )
    return {"message":"user deleted successfully"}    
    


def change_password(db:Session , user_id:int, old_password:str, new_password:str, background_tasks:BackgroundTasks):
    user = get_user_by_id(db,user_id)
    if not user or not verify_password(old_password, user.password):
        logger.warning("Password change failed - invalid credentials", extra={"user_id": user_id})
        raise HTTPException(status_code=401, detail="invalid credentials")
    
    user.password= hash_password(new_password)
    db.commit()
    db.refresh(user)
    logger.info("Password changed successfully", extra={"user_id": user.id})
    log_activity(
        db=db,
        actor_id=user.id,
        action="PASSWORD_CREATED",
        entity_type="USER",
        entity_id=user.id,
        description="Password changed by user"
    )
    send_password_change_email(user.email, background_tasks, user.name)

    return {"message":"password updated successfully"}


def role_change(db:Session,admin_id:int, user_id:int, new_role:str, background_tasks:BackgroundTasks):
    admin = get_user_by_id(db, admin_id)
    if admin.role != "admin":
        logger.warning("Role change failed - admin not found", extra={"admin_id": admin_id})
        raise HTTPException(403,"only admin can change the role")
    
    if new_role not in ["employee","admin","manager"]:
        raise HTTPException(400," invalid role")
    
    user= get_user_by_id(db,user_id)
    if not user:
        logger.warning("Role change failed - user not found", extra={"user_id": user_id})
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_role not in ["employee", "admin", "manager"]:
        logger.warning("Role change failed - invalid role", extra={"user_id": user_id, "new_role": new_role})
        raise HTTPException(status_code=400, detail="Invalid role")
    user.role= new_role
    db.commit()
    db.refresh(user)
    logger.info("User role changed", extra={"user_id": user.id, "new_role": new_role, "changed_by": admin.id})

    log_activity(
        db=db,
        actor_id=admin.id,
        action="ROLE_UPDATED",
        entity_type="USER",
        entity_id=user.id,
        description="user's role updated"
    )
    send_role_change_email(user.email, background_tasks, user.name, new_role)
    return user
         


