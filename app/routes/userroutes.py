from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schema import UserCreate, UserResponse
from app.db.session import get_db
from app.services.auth import sign_up, login

router = APIRouter(prefix="/auth", tags=["Auth"])

# Signup endpoint
@router.post("/signup", response_model=UserResponse)
def signup_route(user: UserCreate, db: Session = Depends(get_db)):
    return sign_up(db, user)

# Login endpoint
@router.post("/login", response_model=UserResponse)
def login_route(user: UserCreate, db: Session = Depends(get_db)):
    return login(db, user.email, user.password)
