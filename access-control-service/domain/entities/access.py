"""
Access entity - Core business model
"""
from datetime import datetime
from typing import Optional


class Access:
    """Access domain entity"""
    
    def __init__(
        self,
        employee_id: str,
        access_datetime: datetime,
        id: Optional[int] = None,
        exit_datetime: Optional[datetime] = None,
        duration_minutes: Optional[int] = None
    ):
        self.id = id
        self.employee_id = employee_id
        self.access_datetime = access_datetime
        self.exit_datetime = exit_datetime
        self.duration_minutes = duration_minutes
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'access_datetime': self.access_datetime.isoformat() if self.access_datetime else None,
            'exit_datetime': self.exit_datetime.isoformat() if self.exit_datetime else None,
            'duration_minutes': self.duration_minutes
        }
    
    def is_active(self) -> bool:
        """Check if access is still active (no exit)"""
        return self.exit_datetime is None
    
    def calculate_duration(self) -> Optional[int]:
        """Calculate duration in minutes"""
        if self.exit_datetime and self.access_datetime:
            delta = self.exit_datetime - self.access_datetime
            return int(delta.total_seconds() / 60)
        return None
    
    def register_exit(self, exit_datetime: datetime):
        """Register exit and calculate duration"""
        self.exit_datetime = exit_datetime
        self.duration_minutes = self.calculate_duration()
