from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class Employee(BaseModel):
    document: str = Field(..., description="Employee document ID (Primary Key)")
    firstname: str = Field(..., min_length=1, max_length=100)
    lastname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., description="Employee email address")
    phone: str = Field(..., min_length=7, max_length=15)
    status: bool = Field(default=True, description="True=Active, False=Inactive")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "document": "1234567890",
                "firstname": "Juan",
                "lastname": "Pérez",
                "email": "juan.perez@example.com",
                "phone": "3001234567",
                "status": True
            }
        }

class EmployeeCreate(BaseModel):
    document: str
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    status: bool = True

class EmployeeUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[bool] = None

class EmployeeResponse(BaseModel):
    document: str
    firstname: str
    lastname: str
    email: str
    phone: str
    status: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
