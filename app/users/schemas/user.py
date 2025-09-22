from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOutput(BaseModel):
    name: str
    email: str
    

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
