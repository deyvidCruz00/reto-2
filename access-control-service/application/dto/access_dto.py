from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class CheckInRequestDTO(BaseModel):
    """DTO for check-in request"""
    employee_id: str = Field(..., alias='employeeId', min_length=1, max_length=50)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "employeeId": "1234567890"
            }
        }


class CheckOutRequestDTO(BaseModel):
    """DTO for check-out request"""
    employee_id: str = Field(..., alias='employeeId', min_length=1, max_length=50)
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "employeeId": "1234567890"
            }
        }


class AccessResponseDTO(BaseModel):
    """DTO for access operation response"""
    success: bool
    message: str
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Check-in registered successfully",
                "data": {
                    "id": "507f1f77bcf86cd799439011",
                    "employee_id": "1234567890",
                    "access_datetime": "2024-11-12 08:30:00",
                    "exit_datetime": None,
                    "duration_minutes": None
                }
            }
        }


class AccessReportDTO(BaseModel):
    """DTO for access report item"""
    employee_id: str
    access_datetime: str
    exit_datetime: Optional[str] = None
    duration_minutes: Optional[int] = None
    duration_hours: Optional[str] = None
    date: Optional[str] = None
    access_time: Optional[str] = None
    exit_time: Optional[str] = None


class DateQueryDTO(BaseModel):
    """DTO for date query parameter"""
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in format YYYY-MM-DD')
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-11-12"
            }
        }


class DateRangeQueryDTO(BaseModel):
    """DTO for date range query parameters"""
    employee_id: str = Field(..., alias='employeeId', min_length=1, max_length=50)
    start_date: str = Field(..., alias='startDate', pattern=r'^\d{4}-\d{2}-\d{2}$')
    end_date: str = Field(..., alias='endDate', pattern=r'^\d{4}-\d{2}-\d{2}$')
    
    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in format YYYY-MM-DD')
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "employeeId": "1234567890",
                "startDate": "2024-11-01",
                "endDate": "2024-11-30"
            }
        }


class SagaAccessRequestDTO(BaseModel):
    """DTO for SAGA access registration request from orchestrator"""
    saga_id: str = Field(..., alias='sagaId')
    employee_id: str = Field(..., alias='employeeId')
    employee_name: str = Field(default='', alias='employeeName')
    action: str = Field(default='CHECK_IN')
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "sagaId": "saga-12345",
                "employeeId": "1234567890",
                "employeeName": "John Doe",
                "action": "CHECK_IN"
            }
        }


class SagaAccessResponseDTO(BaseModel):
    """DTO for SAGA access registration response to orchestrator"""
    saga_id: str = Field(..., alias='sagaId')
    success: bool
    access_id: Optional[str] = Field(None, alias='accessId')
    error_message: Optional[str] = Field(None, alias='errorMessage')
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "sagaId": "saga-12345",
                "success": True,
                "accessId": "507f1f77bcf86cd799439011",
                "errorMessage": None
            }
        }
