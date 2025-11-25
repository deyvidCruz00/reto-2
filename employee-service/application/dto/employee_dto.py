"""
Data Transfer Objects for Employee Service
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from typing import Optional, Union
from datetime import datetime


class EmployeeCreateDTO(BaseModel):
    """DTO for creating an employee"""
    document: str
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    status: bool = True


class EmployeeUpdateDTO(BaseModel):
    """DTO for updating an employee"""
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[bool] = None


class EmployeeResponseDTO(BaseModel):
    """DTO for employee response with camelCase for frontend compatibility"""
    model_config = ConfigDict(populate_by_name=True)
    
    document: str = Field(serialization_alias='documentNumber')
    firstname: str = Field(serialization_alias='firstName')
    lastname: str = Field(serialization_alias='lastName')
    email: str = Field(serialization_alias='email')
    phone: str = Field(serialization_alias='phoneNumber')
    status: bool = Field(serialization_alias='status')
    created_at: Optional[Union[datetime, str]] = Field(default=None, serialization_alias='createdAt')
    updated_at: Optional[Union[datetime, str]] = Field(default=None, serialization_alias='updatedAt')
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: Union[datetime, str, None]) -> Optional[str]:
        """Convert datetime to ISO string"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)


class EmployeeValidationRequestDTO(BaseModel):
    """DTO for SAGA employee validation request"""
    sagaId: str
    employeeId: str
    action: Optional[str] = None


class EmployeeValidationResponseDTO(BaseModel):
    """DTO for SAGA employee validation response"""
    sagaId: str
    isValid: bool
    employeeName: str
    errorMessage: str = ""
