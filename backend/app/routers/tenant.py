from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"]
)


# GET all tenants
@router.get("/")
def get_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()


# GET one tenant
@router.get("/{tenant_id}")
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    return tenant


# POST create tenant
@router.post("/")
def create_tenant(
    tenant: TenantCreate,
    db: Session = Depends(get_db)
):
    db_tenant = Tenant(
        name=tenant.name,
        slug=tenant.slug
    )

    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)

    return db_tenant


# PUT update tenant
@router.put("/{tenant_id}")
def update_tenant(
    tenant_id: int,
    tenant: TenantUpdate,
    db: Session = Depends(get_db)
):
    db_tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not db_tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    db_tenant.name = tenant.name
    db_tenant.slug = tenant.slug

    db.commit()
    db.refresh(db_tenant)

    return db_tenant

# DELETE tenant
@router.delete("/{tenant_id}")
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    db_tenant = db.query(Tenant).filter(
        Tenant.id == tenant_id
    ).first()

    if not db_tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    db.delete(db_tenant)
    db.commit()

    return {
        "message": "Tenant deleted successfully",
        "tenant_id": tenant_id
    }