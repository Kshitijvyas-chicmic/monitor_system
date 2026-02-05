from fastapi import HTTPException, status
from app.models.user import User
from typing import List
from fastapi import Depends
from app.core.jwt import get_current_user
def require_roles(allowed_roles:List[str]):
    def role_checker(current_user:User= Depends(get_current_user)):
        if current_user.role not in allowed_roles:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted for role '{current_user.role}'"
            )
        return current_user
    return role_checker
