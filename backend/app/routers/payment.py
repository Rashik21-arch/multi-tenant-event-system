import asyncio
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models.reservation import Reservation
from app.models.ticket import Ticket
from app.schemas.payment import (
    MockPaymentRequest,
    PaymentResponse
)
from app.auth.security import get_current_user


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ============================================================
# BACKGROUND PAYMENT PROCESSOR
# ============================================================

async def process_payment(
    reservation_id: int,
    payment_success: bool
):

    # Simulate external payment gateway delay
    await asyncio.sleep(3)

    db = SessionLocal()

    try:

        reservation = (
            db.query(Reservation)
            .filter(Reservation.id == reservation_id)
            .with_for_update()
            .first()
        )

        if not reservation:
            return

        # Reservation already processed
        if reservation.status != "HELD":
            return

        # Check whether hold expired
        if (
            reservation.hold_expires_at
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
            reservation.payment_status = "FAILED"

            db.commit()
            return

        # ====================================================
        # PAYMENT SUCCESS
        # ====================================================

        if payment_success:

            reservation.payment_status = "SUCCESS"
            reservation.status = "CONFIRMED"

            db.commit()

            print(
                f"Payment successful for reservation {reservation_id}"
            )

        # ====================================================
        # PAYMENT FAILED
        # ====================================================

        else:

            ticket = (
                db.query(Ticket)
                .filter(Ticket.id == reservation.ticket_id)
                .with_for_update()
                .first()
            )

            if ticket:
                ticket.quantity += reservation.quantity

            reservation.payment_status = "FAILED"
            reservation.status = "PAYMENT_FAILED"

            db.commit()

            print(
                f"Payment failed for reservation {reservation_id}"
            )

    except Exception as e:

        db.rollback()

        print(
            f"Payment processing error: {e}"
        )

    finally:

        db.close()


# ============================================================
# START MOCK PAYMENT
# ============================================================

@router.post(
    "/{reservation_id}",
    response_model=PaymentResponse
)
def make_payment(
    reservation_id: int,
    payment_data: MockPaymentRequest,
    background_tasks: BackgroundTasks,
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

    if reservation.status != "HELD":
        raise HTTPException(
            status_code=400,
            detail=f"Reservation cannot be paid because status is {reservation.status}"
        )

    if (
        reservation.hold_expires_at
        and reservation.hold_expires_at < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=400,
            detail="Reservation hold has expired"
        )

    if reservation.payment_status == "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Payment already completed"
        )

    # Mark payment as pending
    reservation.payment_status = "PENDING"

    db.commit()

    # Run payment asynchronously
    background_tasks.add_task(
        process_payment,
        reservation_id,
        payment_data.success
    )

    return {
        "reservation_id": reservation_id,
        "payment_status": "PENDING",
        "reservation_status": "HELD",
        "message": "Payment processing started"
    }