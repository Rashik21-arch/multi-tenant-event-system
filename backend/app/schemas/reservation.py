from pydantic import BaseModel, EmailStr
from datetime import datetime


class ReservationBase(BaseModel):
    ticket_id: int
    customer_name: str
    customer_email: EmailStr
    quantity: int


class ReservationCreate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int
    total_price: float
    status: str
    payment_status:str
    created_at: datetime
    hold_expires_at: datetime | None = None

    class Config:
        from_attributes = True