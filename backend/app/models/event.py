from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)
    event_date = Column(DateTime, nullable=False)

    tenant = relationship("Tenant", back_populates="events")
    
    tickets = relationship(
    "Ticket",
    back_populates="event",
    cascade="all, delete-orphan"
)