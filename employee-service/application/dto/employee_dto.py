"""
Data Transfer Objects for Employee Service
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


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
    """DTO for employee response"""
    document: str
    firstname: str
    lastname: str
    email: str
    phone: str
    status: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


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
