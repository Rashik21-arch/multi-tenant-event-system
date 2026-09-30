from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    tenant_id: int
    name: str
    description: str | None = None
    location: str | None = None
    event_date: datetime


class EventResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    description: str | None = None
    location: str | None = None
    event_date: datetime

    class Config:
        from_attributes = True