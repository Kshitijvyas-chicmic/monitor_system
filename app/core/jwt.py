from datetime import datetime, timedelta
from app.core.config import JWT_SECRET_KEY,JWT_ALGORITHM
from jose import jwt ,JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from app.models.user import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES=60

def create_access_token(data:dict):
    to_encode = data.copy()
    expire= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:str= Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])

        user_id:str = payload.get("sub")
        role:str= payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        db = SessionLocal()
        user = db.query(User).filter(User.id== int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.role = role
        return user
    
    except JWTError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
