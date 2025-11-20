"""
Port interfaces for Employee Service - Hexagonal Architecture
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from domain.entities.employee import Employee


class EmployeeRepositoryPort(ABC):
    """Port for employee repository (output port)"""
    
    @abstractmethod
    def create(self, employee_data: Dict) -> Employee:
        """Create a new employee"""
        pass
    
    @abstractmethod
    def find_by_document(self, document: str) -> Optional[Employee]:
        """Find employee by document"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Employee]:
        """Find all employees"""
        pass
    
    @abstractmethod
    def update(self, document: str, employee_data: Dict) -> Optional[Employee]:
        """Update an employee"""
        pass
    
    @abstractmethod
    def delete(self, document: str) -> bool:
        """Delete an employee"""
        pass
    
    @abstractmethod
    def exists(self, document: str) -> bool:
        """Check if employee exists"""
        pass
    
    @abstractmethod
    def is_active(self, document: str) -> bool:
        """Check if employee is active"""
        pass


class EventPublisherPort(ABC):
    """Port for publishing events (output port)"""
    
    @abstractmethod
    def publish_employee_created(self, employee: Employee) -> None:
        """Publish employee created event"""
        pass
    
    @abstractmethod
    def publish_employee_updated(self, employee: Employee) -> None:
        """Publish employee updated event"""
        pass
    
    @abstractmethod
    def publish_employee_validation_response(self, validation_result: Dict) -> None:
        """Publish employee validation response for SAGA"""
        pass


class EmployeeUseCasePort(ABC):
    """Port for employee use cases (input port)"""
    
    @abstractmethod
    def create_employee(self, employee_data: Dict) -> Dict:
        """Create a new employee"""
        pass
    
    @abstractmethod
    def update_employee(self, employee_data: Dict) -> Dict:
        """Update an employee"""
        pass
    
    @abstractmethod
    def find_all_employees(self) -> Dict:
        """Find all employees"""
        pass
    
    @abstractmethod
    def find_employee_by_document(self, document: str) -> Dict:
        """Find employee by document"""
        pass
    
    @abstractmethod
    def delete_employee(self, document: str) -> Dict:
        """Delete an employee"""
        pass
    
    @abstractmethod
    def validate_employee(self, document: str) -> Dict:
        """Validate employee for SAGA"""
        pass
