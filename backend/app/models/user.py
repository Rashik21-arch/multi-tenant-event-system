from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    hashed_password = Column(String, nullable=False)

    role = Column(String, nullable=False, default="Attendee")

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=True)

    is_active = Column(Boolean, default=True)

    tenant = relationship("Tenant")