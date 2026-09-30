from datetime import datetime

from app.database import SessionLocal
from app.models.reservation import Reservation
from app.models.ticket import Ticket


def release_expired_holds():
    db = SessionLocal()

    try:
        expired_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.status == "HELD",
                Reservation.hold_expires_at <= datetime.utcnow()
            )
            .with_for_update()
            .all()
        )

        for reservation in expired_reservations:

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

        if expired_reservations:
            print(
                f"Released {len(expired_reservations)} expired reservation(s)"
            )

    except Exception as e:
        db.rollback()
        print(f"Hold expiry error: {e}")

    finally:
        db.close()