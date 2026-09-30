from datetime import datetime
from pydantic import BaseModel


class TicketBase(BaseModel):
    event_id: int
    name: str
    price: float
    quantity: int


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    event_id: int
    name: str
    price: float
    quantity: int


class TicketResponse(TicketBase):
    id: int

    class Config:
        from_attributes = True