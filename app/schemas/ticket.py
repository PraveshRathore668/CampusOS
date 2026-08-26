from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.ticket import CategoryEnum, PriorityEnum, StatusEnum


class TicketCreate(BaseModel):
    title: str
    description: str
    location: str
    category: Optional[CategoryEnum] = None
    priority: Optional[PriorityEnum] = None


class TicketUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    assigned_admin: Optional[int] = None
    priority: Optional[PriorityEnum] = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    location: str
    category: CategoryEnum
    priority: PriorityEnum
    status: StatusEnum
    created_by: int
    assigned_admin: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
