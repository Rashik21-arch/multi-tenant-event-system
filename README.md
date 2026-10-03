# Multi-Tenant Event & Ticket Reservation System

A full-stack multi-tenant event and ticket reservation platform built with FastAPI, PostgreSQL, Redis, SQLAlchemy, React, and Vite.

## 🚀 Live Demo

### Frontend
https://multi-tenant-event-frontend.onrender.com

### Backend API
https://multi-tenant-event-system.onrender.com

### Swagger API Documentation
https://multi-tenant-event-system.onrender.com/docs

### GitHub
https://github.com/Rashik21-arch/multi-tenant-event-system

---

## 📌 Features

- Multi-tenant architecture
- Role-Based Access Control (RBAC)
- Admin, Organizer and Attendee roles
- JWT authentication
- Event creation and management
- Ticket tier management
- Ticket quantity management
- Temporary ticket reservation holds
- 10-minute reservation expiry
- Mock asynchronous payment gateway
- Reservation confirmation and cancellation
- PostgreSQL database
- SQLAlchemy ORM
- Redis integration
- Redis caching for active event data
- Background job for expired reservation holds
- Analytics dashboard
- Revenue tracking
- Ticket conversion rate
- React + Vite frontend
- REST API
- Swagger/OpenAPI documentation

---

## 🛠️ Technology Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Pydantic
- JWT Authentication
- Passlib/Bcrypt
- APScheduler

### Frontend
- React
- Vite
- JavaScript
- CSS

### Deployment
- Render
- Render PostgreSQL
- Render Redis

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │   React Frontend    │
                 │      Vite           │
                 └──────────┬──────────┘
                            │ REST API
                            ▼
                 ┌─────────────────────┐
                 │   FastAPI Backend   │
                 │                     │
                 │ Authentication      │
                 │ RBAC                │
                 │ Events              │
                 │ Tickets             │
                 │ Reservations        │
                 │ Payments            │
                 │ Analytics           │
                 └──────┬──────┬───────┘
                        │      │
              ┌─────────┘      └──────────┐
              ▼                            ▼
      ┌───────────────┐            ┌───────────────┐
      │  PostgreSQL   │            │     Redis     │
      │   Database    │            │ Cache/Locks   │
      └───────────────┘            └───────────────┘

      👥 User Roles
Admin
Manage tenants
Manage users and system resources
Access administrative functionality
Organizer
Create events
Update events
Create ticket types
Manage ticket quantities
View event-related analytics
Attendee
View events
View available tickets
Create reservations
Complete mock payments
View reservation status
🎟️ Reservation Flow
Select Event
     ↓
Select Ticket
     ↓
Create Reservation
     ↓
Ticket Status = HELD
     ↓
10-Minute Hold
     ↓
Payment
  ↙       ↘
Success   Expired
  ↓          ↓
CONFIRMED   EXPIRED

The reservation system temporarily holds tickets before payment. Expired holds are released by the background expiry process.

📊 Analytics

The dashboard provides:

Total reservations
Confirmed reservations
Held reservations
Expired reservations
Total revenue
Ticket conversion rate

Example production result:

Total Reservations: 1
Confirmed:           1
Held:                0
Expired:             0
Revenue:             ₹3000
Conversion Rate:     100%
🔐 Authentication

Authentication uses JWT access tokens.

Protected API endpoints require:

Authorization: Bearer <access_token>

Role-based access control restricts operations according to the user's role.

🗄️ Database

Main entities:

Tenant
User
Event
Ticket
Reservation
Payment

The ER diagram is available at:

docs/ER-DIAGRAM.md
📮 API Testing

Swagger documentation:

https://multi-tenant-event-system.onrender.com/docs

Postman collection:

postman/Multi-tenant Event & Ticket Reservation System.postman_collection.json

The API can be tested for:

Authentication
Event management
Ticket management
Reservations
Payments
Analytics
Authorization/RBAC
Reservation expiry
Error handling
💻 Local Development
Backend
cd backend

Create and activate a virtual environment:

python -m venv .venv

Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the backend:

python -m uvicorn app.main:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
Frontend
cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173
🐳 Redis

For local development:

docker run -d --name event-redis -p 6379:6379 redis:7
📁 Project Structure
multi-tenant-event-system/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── ER-DIAGRAM.md
│
├── postman/
│   └── Multi-tenant Event & Ticket Reservation System.postman_collection.json
│
├── openapi.json
├── README.md
└── .gitignore
☁️ Deployment

The application is deployed using Render.

Production Services
React frontend — Render Static Site
FastAPI backend — Render Web Service
PostgreSQL — Render PostgreSQL
Redis — Render Key Value
Production URLs

Frontend:

https://multi-tenant-event-frontend.onrender.com

Backend:

https://multi-tenant-event-system.onrender.com

Swagger:

https://multi-tenant-event-system.onrender.com/docs

🧪 Production Verification

The deployed application was verified with:

User registration/login
JWT authentication
Organizer event creation
Ticket creation
Reservation creation
Mock payment
Reservation confirmation
Analytics calculation
React frontend/backend connectivity

Production test example:

Event: Chengalpattu Tech Fest 2026
Ticket: VIP Ticket
Ticket Price: ₹1500
Reserved Quantity: 2
Total: ₹3000
Payment: SUCCESS
Reservation: CONFIRMED