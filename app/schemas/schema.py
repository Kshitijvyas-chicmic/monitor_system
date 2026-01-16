from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    eamil:EmailStr
    role:str

    class Config:
        orm_mode= True