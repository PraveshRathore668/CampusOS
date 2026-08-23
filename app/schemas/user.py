from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: RoleEnum = RoleEnum.STUDENT


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True
