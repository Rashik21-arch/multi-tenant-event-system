from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import redis
import json

from app.database import get_db
from app.models.event import Event
from app.models.tenant import Tenant
from app.schemas.event import EventCreate, EventResponse
from app.auth.security import require_roles


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# ============================================================
# REDIS CONFIGURATION
# ============================================================

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


# ============================================================
# GET ALL EVENTS
# ============================================================

@router.get("/", response_model=list[EventResponse])
def get_events(
    db: Session = Depends(get_db)
):

    cache_key = "events:all"

    # --------------------------------------------------------
    # 1. Check Redis cache
    # --------------------------------------------------------

    try:
        cached_events = redis_client.get(cache_key)

        if cached_events:
            return json.loads(cached_events)

    except Exception:
        # Redis unavailable -> continue with PostgreSQL
        pass

    # --------------------------------------------------------
    # 2. Get events from PostgreSQL
    # --------------------------------------------------------

    events = db.query(Event).all()

    # --------------------------------------------------------
    # 3. Store events in Redis
    # --------------------------------------------------------

    try:

        events_data = [
            {
                "id": event.id,
                "tenant_id": event.tenant_id,
                "name": event.name,
                "description": event.description,
                "location": event.location,
                "event_date": (
                    event.event_date.isoformat()
                    if event.event_date
                    else None
                )
            }
            for event in events
        ]

        # Cache for 5 minutes
        redis_client.setex(
            cache_key,
            300,
            json.dumps(events_data)
        )

    except Exception:
        pass

    return events


# ============================================================
# GET ONE EVENT
# ============================================================

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    cache_key = f"event:{event_id}"

    # --------------------------------------------------------
    # 1. Check Redis
    # --------------------------------------------------------

    try:

        cached_event = redis_client.get(cache_key)

        if cached_event:
            return json.loads(cached_event)

    except Exception:
        pass

    # --------------------------------------------------------
    # 2. Get event from PostgreSQL
    # --------------------------------------------------------

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # --------------------------------------------------------
    # 3. Convert event to dictionary
    # --------------------------------------------------------

    event_data = {
        "id": event.id,
        "tenant_id": event.tenant_id,
        "name": event.name,
        "description": event.description,
        "location": event.location,
        "event_date": (
            event.event_date.isoformat()
            if event.event_date
            else None
        )
    }

    # --------------------------------------------------------
    # 4. Store in Redis for 5 minutes
    # --------------------------------------------------------

    try:

        redis_client.setex(
            cache_key,
            300,
            json.dumps(event_data)
        )

    except Exception:
        pass

    return event_data


# ============================================================
# CREATE EVENT
# ============================================================

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("Admin", "Organizer")
    )
):

    # --------------------------------------------------------
    # Check whether tenant exists
    # --------------------------------------------------------

    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == event.tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    # --------------------------------------------------------
    # Create event
    # --------------------------------------------------------

    new_event = Event(
        tenant_id=event.tenant_id,
        name=event.name,
        description=event.description,
        location=event.location,
        event_date=event.event_date
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # --------------------------------------------------------
    # Invalidate all-events cache
    # --------------------------------------------------------

    try:
        redis_client.delete("events:all")
    except Exception:
        pass

    return new_event


# ============================================================
# UPDATE EVENT
# ============================================================

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("Admin", "Organizer")
    )
):

    # --------------------------------------------------------
    # Find event
    # --------------------------------------------------------

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # --------------------------------------------------------
    # Check tenant
    # --------------------------------------------------------

    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == event_data.tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    # --------------------------------------------------------
    # Update event
    # --------------------------------------------------------

    event.tenant_id = event_data.tenant_id
    event.name = event_data.name
    event.description = event_data.description
    event.location = event_data.location
    event.event_date = event_data.event_date

    db.commit()
    db.refresh(event)

    # --------------------------------------------------------
    # Invalidate Redis caches
    # --------------------------------------------------------

    try:

        redis_client.delete(
            f"event:{event_id}",
            "events:all"
        )

    except Exception:
        pass

    return event


# ============================================================
# DELETE EVENT
# ============================================================

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles("Admin", "Organizer")
    )
):

    # --------------------------------------------------------
    # Find event
    # --------------------------------------------------------

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    # --------------------------------------------------------
    # Delete event
    # --------------------------------------------------------

    db.delete(event)
    db.commit()

    # --------------------------------------------------------
    # Remove from Redis
    # --------------------------------------------------------

    try:

        redis_client.delete(
            f"event:{event_id}",
            "events:all"
        )

    except Exception:
        pass

    return {
        "message": "Event deleted successfully",
        "event_id": event_id
    }