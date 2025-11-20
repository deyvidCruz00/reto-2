"""
Employee entity - Core business model
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class Employee(BaseModel):
    """Employee domain entity"""
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
    
    @property
    def full_name(self) -> str:
        """Get full name of employee"""
        return f"{self.firstname} {self.lastname}"
    
    def is_active(self) -> bool:
        """Check if employee is active"""
        return self.status
