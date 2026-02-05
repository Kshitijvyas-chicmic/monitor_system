from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.schema import UserCreate, UserResponse , UserUpadte ,UpdateRoleSchema,PasswordChange, LoginRequest
from typing import List
from app.db.session import get_db
from app.services.auth import sign_up, login, get_all_user, get_user_by_id, update_user, delete_user, role_change
from app.core.jwt import get_current_user
from app.services.auth import change_password
from fastapi import HTTPException, status
from app.models.user import User
from app.core.rate_limiter import limiter


from app.core.role_core import require_roles
router = APIRouter(prefix="/auth", tags=["Auth"])

# Signup endpoint
@router.post("/signup", response_model=UserResponse)
@limiter.limit("5/minute")
def signup_route(request:Request,user: UserCreate, db: Session = Depends(get_db)):
    return sign_up(db, user)

# Login endpoint
@router.post("/login")
@limiter.limit("10/minute")
def login_route( request: Request, user: LoginRequest, db: Session = Depends(get_db)):
    return login(db, user.email, user.password)


# list all users only admin can access
@router.get("/",response_model=list[UserResponse])
@limiter.limit("10/minute")
def list_users( request: Request, db:Session = Depends(get_db),
        current_user:User= Depends(require_roles(["admin"]))):
    return get_all_user(db)

# get single user aonly admin and user
@router.get("/user_id/{user_id}",response_model=UserResponse)
@limiter.limit("20/minute")
def get_user( request: Request, user_id:int , db:Session = Depends(get_db), current_user:User= Depends(get_current_user)):
    if current_user.role!= "admin" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail ="operation not permitted")
    return get_user_by_id(db,user_id)

# update user only user
@router.put("/user_id/{user_id}",response_model=UserResponse)
@limiter.limit("10/minute")
def update_user_route( request: Request, user_id:int, data:UserUpadte , db:Session = Depends(get_db), current_user:User= Depends(get_current_user)):
     if current_user.id != user_id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
     return update_user(db,user_id,data)

# delete user only admin can change it

@router.delete("/user_id/{user_id}")
@limiter.limit("3/minute")
def delete_user_route( request: Request, user_id:int , db:Session = Depends(get_db), current_user:User= Depends(require_roles(["admin"]))):
    return delete_user(db,user_id, current_user)

# change password 
@router.put("/change-password/{user_id}")
@limiter.limit("5/minute")
def change_password_route( request: Request, user_id:int,
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
     if current_user.id != user_id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
     return change_password(db, current_user.id, data.old_password, data.new_password)


# role change only admin can change the role 
@router.patch("/{user_id}/role", response_model=UserResponse)
@limiter.limit("5/minute")
def patch_user_role( request: Request, user_id:int, data:UpdateRoleSchema, db:Session=Depends(get_db), current_user:User= Depends(require_roles(["admin"]))):
    return role_change(db,current_user.id,user_id,data.role)