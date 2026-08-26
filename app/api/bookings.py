from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from database import get_db
from app.models.booking import Booking, Resource
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingOut, ResourceOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.get("/resources", response_model=List[ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = db.query(Resource).filter(Resource.id == booking_in.resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    new_booking = Booking(
        resource_id=booking_in.resource_id,
        booked_by=current_user.id,
        start_time=booking_in.start_time,
        end_time=booking_in.end_time,
    )
    db.add(new_booking)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This resource is already booked for the selected time slot",
        )

    db.refresh(new_booking)
    return new_booking


@router.get("", response_model=List[BookingOut])
def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Booking).filter(Booking.booked_by == current_user.id).all()
