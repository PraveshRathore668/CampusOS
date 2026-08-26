import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ResourceTypeEnum(str, enum.Enum):
    LAB = "LAB"
    ROOM = "ROOM"
    SPORTS_FACILITY = "SPORTS_FACILITY"


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    resource_type = Column(Enum(ResourceTypeEnum), nullable=False)
    location = Column(String, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    booked_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resource = relationship("Resource")
    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("resource_id", "start_time", name="uq_resource_start_time"),
    )
