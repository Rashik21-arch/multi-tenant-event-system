from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.ticket import Ticket
from app.models.reservation import Reservation
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse
)
from app.auth.security import get_current_user


router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


# ============================================================
# CREATE 10-MINUTE HOLD
# ============================================================

@router.post(
    "/",
    response_model=ReservationResponse
)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Basic validation
    if reservation_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # --------------------------------------------------------
    # Lock the ticket row
    # --------------------------------------------------------
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == reservation_data.ticket_id)
        .with_for_update()
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    # --------------------------------------------------------
    # Check available tickets
    # --------------------------------------------------------
    if ticket.quantity < reservation_data.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Only {ticket.quantity} tickets available"
        )

    # --------------------------------------------------------
    # Reserve tickets
    # --------------------------------------------------------
    ticket.quantity -= reservation_data.quantity

    # 10-minute hold
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    total_price = (
        ticket.price * reservation_data.quantity
    )

    reservation = Reservation(
        ticket_id=ticket.id,
        customer_name=reservation_data.customer_name,
        customer_email=reservation_data.customer_email,
        quantity=reservation_data.quantity,
        total_price=total_price,
        status="HELD",
        created_at=datetime.utcnow(),
        hold_expires_at=expires_at
    )

    db.add(reservation)

    try:
        db.commit()
        db.refresh(reservation)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Could not create reservation"
        )

    return reservation


# ============================================================
# GET ALL RESERVATIONS
# ============================================================

@router.get(
    "/",
    response_model=list[ReservationResponse]
)
def get_reservations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(Reservation).all()


# ============================================================
# GET SINGLE RESERVATION
# ============================================================

@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse
)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id)
        .first()
    )

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    # --------------------------------------------------------
    # Automatically detect expired hold
    # --------------------------------------------------------

    if (
        reservation.status == "HELD"
        and reservation.hold_expires_at
        and reservation.hold_expires_at < datetime.utcnow()
    ):

        ticket = (
            db.query(Ticket)
            .filter(Ticket.id == reservation.ticket_id)
            .with_for_update()
            .first()
        )

        if ticket:
            ticket.quantity += reservation.quantity

        reservation.status = "EXPIRED"

        db.commit()
        db.refresh(reservation)

    return reservation


# ============================================================
# CANCEL RESERVATION
# ============================================================

@router.delete(
    "/{reservation_id}"
)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    reservation = (
        db.query(Reservation)
        .filter(Reservation.id == reservation_id)
        .with_for_update()
        .first()
    )

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservation not found"
        )

    # --------------------------------------------------------
    # Release ticket stock only if reservation is still HELD
    # --------------------------------------------------------

    if reservation.status == "HELD":

        ticket = (
            db.query(Ticket)
            .filter(Ticket.id == reservation.ticket_id)
            .with_for_update()
            .first()
        )

        if ticket:
            ticket.quantity += reservation.quantity

        reservation.status = "CANCELLED"

        db.commit()

        return {
            "message": "Reservation cancelled",
            "tickets_released": reservation.quantity
        }

    raise HTTPException(
        status_code=400,
        detail=f"Reservation cannot be cancelled because status is {reservation.status}"
    )