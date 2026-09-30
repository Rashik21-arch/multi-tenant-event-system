from pydantic import BaseModel


class TenantCreate(BaseModel):
    name: str
    slug: str

class TenantUpdate(BaseModel):
    name: str
    slug: str