from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class OwnerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class OwnerCreate(OwnerBase):
    pass


class Owner(OwnerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PropertyBase(BaseModel):
    property_name: str = Field(..., min_length=1,
                               max_length=255, description="Name of the property")
    address: str
    city: str
    state: str
    zip_code: str
    monthly_rent: float = Field(
        gt=0, description="Monthly rent must be greater than 0")
    status: str = "VACANT"


class PropertyCreate(PropertyBase):
    owner_id: int


class Property(PropertyBase):
    id: int
    owner_id: int
    current_tenant_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
