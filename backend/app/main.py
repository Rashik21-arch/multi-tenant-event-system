from fastapi import FastAPI
from sqlalchemy import text

from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models.tenant import Tenant
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.reservation import Reservation
from app.models.user import User
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.hold_expiry import release_expired_holds
from app.routers.event import router as event_router
from app.routers.ticket import router as ticket_router
from app.routers.reservation import router as reservation_router
from app.routers.tenant import router as tenant_router
from app.auth.router import router as auth_router
from app.routers.payment import router as payment_router
from app.routers.analytics import router as analytics_router

scheduler = BackgroundScheduler()

scheduler.add_job(
    release_expired_holds,
    "interval",
    seconds=30
)

scheduler.start()
app = FastAPI(
    title="Multi-Tenant Event & Ticket Reservation System",
    description="Full Stack Event and Ticket Reservation Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "https://multi-tenant-event-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(event_router)
app.include_router(ticket_router)
app.include_router(reservation_router)
app.include_router(tenant_router)
app.include_router(auth_router)
app.include_router(payment_router)
app.include_router(analytics_router)

@app.get("/")
def root():
    return {
        "message": "Event Reservation API is running"
    }

@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e)
        }