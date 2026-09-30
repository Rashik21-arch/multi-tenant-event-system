# Multi-Tenant Event & Ticket Reservation System

A full-stack multi-tenant event and ticket reservation platform built with FastAPI, PostgreSQL, React, Redis, and JWT authentication.

## Features

- Multi-tenant architecture
- JWT authentication
- Role-based access control
- Event management
- Ticket management
- Ticket reservations
- 10-minute temporary ticket holds
- Automatic expiry of unpaid reservations
- Mock asynchronous payment processing
- PostgreSQL database
- Redis caching
- Background job for expired holds
- Analytics dashboard
- Revenue tracking
- Ticket conversion rate
- Swagger/OpenAPI documentation
- Postman API collection
- React frontend

## Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT
- Redis
- APScheduler

### Frontend
- React
- Vite
- JavaScript
- CSS

### API Testing
- Swagger UI
- Postman

## Project Structure

```text
multi-tenant-event-system/
│
├── backend/
│   └── app/
│       ├── auth/
│       ├── models/
│       ├── schemas/
│       ├── routers/
│       ├── services/
│       ├── database.py
│       └── main.py
│
├── frontend/
│
├── docs/
│   └── ER-DIAGRAM.md
│
├── postman/
│   └── Multi-Tenant-Event-Ticket-Reservation.postman_collection.json
│
├── openapi.json
└── README.md