import enum
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class CategoryEnum(str, enum.Enum):
    IT_EQUIPMENT = "IT_EQUIPMENT"
    ELECTRICAL = "ELECTRICAL"
    PLUMBING = "PLUMBING"
    FURNITURE = "FURNITURE"
    CLEANING = "CLEANING"
    OTHER = "OTHER"


class PriorityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class StatusEnum(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False, default=CategoryEnum.OTHER)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.OPEN)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_admin = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    creator = relationship("User", foreign_keys=[created_by])
    admin = relationship("User", foreign_keys=[assigned_admin])
