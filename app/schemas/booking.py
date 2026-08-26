from pydantic import BaseModel
from datetime import datetime
from app.models.booking import ResourceTypeEnum


class BookingCreate(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime


class BookingOut(BaseModel):
    id: int
    resource_id: int
    booked_by: int
    start_time: datetime
    end_time: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ResourceOut(BaseModel):
    id: int
    name: str
    resource_type: ResourceTypeEnum
    location: str

    class Config:
        from_attributes = True
