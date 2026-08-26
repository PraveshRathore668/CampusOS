from pydantic import BaseModel
from app.models.ticket import CategoryEnum, PriorityEnum


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    category_confidence: float
    priority_confidence: float
