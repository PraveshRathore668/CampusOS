from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.models.ticket import Ticket
from app.models.user import User, RoleEnum
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut
from app.api.deps import get_current_user, require_role
from app.ml.predict import predict_ticket_labels

router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])


@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = ticket_in.category
    priority = ticket_in.priority

    if category is None or priority is None:
        combined_text = f"{ticket_in.title}. {ticket_in.description}"
        prediction = predict_ticket_labels(combined_text)

        if category is None:
            category = prediction["category"]
        if priority is None:
            priority = prediction["priority"]

    new_ticket = Ticket(
        title=ticket_in.title,
        description=ticket_in.description,
        location=ticket_in.location,
        category=category,
        priority=priority,
        created_by=current_user.id,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get("", response_model=List[TicketOut])
def list_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Ticket)

    if current_user.role == RoleEnum.STUDENT:
        query = query.filter(Ticket.created_by == current_user.id)

    return query.order_by(Ticket.created_at.desc()).all()


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    if current_user.role == RoleEnum.STUDENT and ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this ticket",
        )

    return ticket


@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.ADMIN, RoleEnum.FACULTY)),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")

    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)

    return ticket
