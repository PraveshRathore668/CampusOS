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


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
