from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from domain.entities.access import Access


class AccessRepositoryPort(ABC):
    """Port for access data persistence operations"""
    
    @abstractmethod
    def create_checkin(self, employee_id: str) -> Access:
        """Create a new check-in record"""
        pass
    
    @abstractmethod
    def create_checkout(self, employee_id: str) -> Optional[Access]:
        """Register check-out for the most recent active entry"""
        pass
    
    @abstractmethod
    def has_active_entry(self, employee_id: str) -> bool:
        """Check if employee has an active entry (no exit_datetime)"""
        pass
    
    @abstractmethod
    def find_by_date(self, target_date: datetime) -> List[Access]:
        """Find all access records for a specific date"""
        pass
    
    @abstractmethod
    def find_by_employee_and_date_range(
        self, 
        employee_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Access]:
        """Find access records for an employee within a date range"""
        pass
    
    @abstractmethod
    def find_all_active(self) -> List[Access]:
        """Find all active access records (employees currently inside)"""
        pass


class EventPublisherPort(ABC):
    """Port for publishing events to Kafka"""
    
    @abstractmethod
    def publish_access_registration_response(self, response: dict) -> None:
        """Publish access registration response to saga orchestrator"""
        pass
    
    @abstractmethod
    def publish_alert(
        self, 
        alert_code: str, 
        description: str, 
        employee_id: Optional[str] = None
    ) -> None:
        """Publish alert event"""
        pass


class AccessUseCasePort(ABC):
    """Port for access control business logic"""
    
    @abstractmethod
    def user_checkin(self, employee_id: str) -> dict:
        """Register user check-in"""
        pass
    
    @abstractmethod
    def user_checkout(self, employee_id: str) -> dict:
        """Register user check-out"""
        pass
    
    @abstractmethod
    def all_employees_by_date(self, date_str: str) -> dict:
        """Get all employees who accessed on a specific date"""
        pass
    
    @abstractmethod
    def employee_by_dates(
        self, 
        employee_id: str, 
        start_date_str: str, 
        end_date_str: str
    ) -> dict:
        """Get employee access report by date range"""
        pass
    
    @abstractmethod
    def get_all_active_accesses(self) -> dict:
        """Get all active access records (employees currently inside)"""
        pass
    
    @abstractmethod
    def process_checkin_request(
        self, 
        saga_id: str, 
        employee_id: str, 
        employee_name: str
    ) -> None:
        """Process check-in request from saga orchestrator"""
        pass
    
    @abstractmethod
    def process_checkout_request(
        self, 
        saga_id: str, 
        employee_id: str, 
        employee_name: str
    ) -> None:
        """Process check-out request from saga orchestrator"""
        pass
