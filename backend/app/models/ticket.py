from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    name = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    quantity = Column(Integer, nullable=False)

    event = relationship(
        "Event",
        back_populates="tickets"
    )

    reservations = relationship(
    "Reservation",
    back_populates="ticket"
)