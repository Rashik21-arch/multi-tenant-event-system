from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.reservation import Reservation

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/")
def get_analytics(
    db: Session = Depends(get_db)
):
    total_reservations = (
        db.query(func.count(Reservation.id))
        .scalar()
    )

    confirmed_reservations = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == "CONFIRMED")
        .scalar()
    )

    held_reservations = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == "HELD")
        .scalar()
    )

    expired_reservations = (
        db.query(func.count(Reservation.id))
        .filter(Reservation.status == "EXPIRED")
        .scalar()
    )

    revenue = (
        db.query(func.coalesce(func.sum(Reservation.total_price), 0))
        .filter(Reservation.status == "CONFIRMED")
        .scalar()
    )

    if total_reservations > 0:
        conversion_rate = (
            confirmed_reservations / total_reservations
        ) * 100
    else:
        conversion_rate = 0

    return {
        "total_reservations": total_reservations,
        "confirmed_reservations": confirmed_reservations,
        "held_reservations": held_reservations,
        "expired_reservations": expired_reservations,
        "revenue": float(revenue),
        "conversion_rate": round(conversion_rate, 2)
    }