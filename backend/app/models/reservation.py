from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False
    )

    customer_name = Column(String, nullable=False)

    customer_email = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    total_price = Column(Float, nullable=False)

    # HELD / CONFIRMED / EXPIRED / CANCELLED
    status = Column(
        String,
        nullable=False,
        default="HELD"
    )

    payment_status = Column(
    String,
    nullable=False,
    default="PENDING"
)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Reservation remains valid until this time
    hold_expires_at = Column(
        DateTime,
        nullable=True
    )

    ticket = relationship(
        "Ticket",
        back_populates="reservations"
    )