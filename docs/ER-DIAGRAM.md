# ER Diagram – Multi-Tenant Event & Ticket Reservation System

```mermaid
erDiagram

    TENANT ||--o{ USER : has
    TENANT ||--o{ EVENT : owns

    USER ||--o{ RESERVATION : makes

    EVENT ||--o{ TICKET : contains

    TICKET ||--o{ RESERVATION : receives

    RESERVATION ||--o| PAYMENT : has


    TENANT {
        int id PK
        string name
        string slug
        boolean is_active
    }

    USER {
        int id PK
        int tenant_id FK
        string name
        string email
        string hashed_password
        string role
        boolean is_active
    }

    EVENT {
        int id PK
        int tenant_id FK
        string name
        string description
        string location
        datetime event_date
    }

    TICKET {
        int id PK
        int event_id FK
        string name
        float price
        int quantity
    }

    RESERVATION {
        int id PK
        int user_id FK
        int ticket_id FK
        string customer_name
        string customer_email
        int quantity
        float total_price
        string status
        string payment_status
        datetime created_at
        datetime hold_expires_at
    }

    PAYMENT {
        int id PK
        int reservation_id FK
        float amount
        string status
        datetime created_at
    }