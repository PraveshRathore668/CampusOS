from pydantic import BaseModel
from app.models.ticket import CategoryEnum, PriorityEnum
from typing import List


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    category_confidence: float
    priority_confidence: float


class ChatRequest(BaseModel):
    question: str


class SourceChunk(BaseModel):
    document_filename: str
    chunk_index: int
    content_preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
