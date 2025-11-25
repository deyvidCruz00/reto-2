from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from typing import Optional, Union
from datetime import datetime


class CheckInRequestDTO(BaseModel):
    """DTO for check-in request"""
    model_config = ConfigDict(populate_by_name=True)
    
    employee_id: str = Field(..., alias='employeeId', min_length=1, max_length=50)


class CheckOutRequestDTO(BaseModel):
    """DTO for check-out request"""
    model_config = ConfigDict(populate_by_name=True)
    
    employee_id: str = Field(..., alias='employeeId', min_length=1, max_length=50)


class AccessRecordResponseDTO(BaseModel):
    """DTO for access record response with camelCase for frontend compatibility"""
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(serialization_alias='id')
    employee_id: str = Field(serialization_alias='employeeId')
    access_datetime: Optional[Union[datetime, str]] = Field(default=None, serialization_alias='accessDatetime')
    exit_datetime: Optional[Union[datetime, str]] = Field(default=None, serialization_alias='exitDatetime')
    duration_minutes: Optional[int] = Field(default=None, serialization_alias='durationMinutes')
    
    @field_serializer('access_datetime', 'exit_datetime')
    def serialize_datetime(self, dt: Union[datetime, str, None], _info) -> Optional[str]:
        """Convert datetime objects to ISO format strings"""
        if dt is None:
            return None
        if isinstance(dt, str):
            return dt
        if isinstance(dt, datetime):
            return dt.isoformat()
        return str(dt)


class AccessResponseDTO(BaseModel):
    """DTO for access operation response"""
    success: bool
    message: str
    data: Optional[dict] = None


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
