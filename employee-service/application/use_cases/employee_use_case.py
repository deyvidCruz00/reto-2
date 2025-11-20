"""
Employee Use Cases - Application Layer
"""
from typing import Dict
from domain.ports.employee_ports import (
    EmployeeUseCasePort,
    EmployeeRepositoryPort,
    EventPublisherPort
)
from domain.entities.employee import Employee
from application.dto.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO
import logging

logger = logging.getLogger(__name__)


class EmployeeUseCase(EmployeeUseCasePort):
    """Implementation of employee use cases"""
    
    def __init__(
        self,
        repository: EmployeeRepositoryPort,
        event_publisher: EventPublisherPort
    ):
        self.repository = repository
        self.event_publisher = event_publisher
    
    def create_employee(self, employee_data: Dict) -> Dict:
        """Create a new employee"""
        try:
            # Validate DTO
            dto = EmployeeCreateDTO(**employee_data)
            
            # Check if employee already exists
            if self.repository.exists(dto.document):
                return {
                    "success": False,
                    "message": f"Employee with document {dto.document} already exists"
                }
            
            # Create employee
            employee = self.repository.create(dto.model_dump())
            
            # Publish event
            self.event_publisher.publish_employee_created(employee)
            
            return {
                "success": True,
                "message": "Employee created successfully",
                "data": employee.model_dump()
            }
        except Exception as e:
            logger.error(f"Error in create_employee: {e}")
            return {
                "success": False,
                "message": f"Error creating employee: {str(e)}"
            }
    
    def update_employee(self, employee_data: Dict) -> Dict:
        """Update an employee"""
        try:
            document = employee_data.get('document')
            if not document:
                return {
                    "success": False,
                    "message": "Document is required"
                }
            
            # Check if employee exists
            if not self.repository.exists(document):
                return {
                    "success": False,
                    "message": f"Employee with document {document} not found"
                }
            
            # Validate DTO (excluding document)
            update_data = {k: v for k, v in employee_data.items() if k != 'document'}
            dto = EmployeeUpdateDTO(**update_data)
            
            # Update employee
            employee = self.repository.update(document, dto.model_dump(exclude_none=True))
            
            if employee:
                # Publish event
                self.event_publisher.publish_employee_updated(employee)
                
                return {
                    "success": True,
                    "message": "Employee updated successfully",
                    "data": employee.model_dump()
                }
            
            return {
                "success": False,
                "message": "Employee not found or no changes made"
            }
        except Exception as e:
            logger.error(f"Error in update_employee: {e}")
            return {
                "success": False,
                "message": f"Error updating employee: {str(e)}"
            }
    
    def find_all_employees(self) -> Dict:
        """Find all employees"""
        try:
            employees = self.repository.find_all()
            return {
                "success": True,
                "message": f"Found {len(employees)} employees",
                "data": [emp.model_dump() for emp in employees],
                "count": len(employees)
            }
        except Exception as e:
            logger.error(f"Error in find_all_employees: {e}")
            return {
                "success": False,
                "message": f"Error finding employees: {str(e)}",
                "data": [],
                "count": 0
            }
    
    def find_employee_by_document(self, document: str) -> Dict:
        """Find employee by document"""
        try:
            employee = self.repository.find_by_document(document)
            
            if employee:
                return {
                    "success": True,
                    "message": "Employee found",
                    "data": employee.model_dump()
                }
            
            return {
                "success": False,
                "message": f"Employee with document {document} not found"
            }
        except Exception as e:
            logger.error(f"Error in find_employee_by_document: {e}")
            return {
                "success": False,
                "message": f"Error finding employee: {str(e)}"
            }
    
    def delete_employee(self, document: str) -> Dict:
        """Delete an employee (soft delete)"""
        try:
            if not self.repository.exists(document):
                return {
                    "success": False,
                    "message": f"Employee with document {document} not found"
                }
            
            # Soft delete (set status to False)
            update_data = {"status": False}
            employee = self.repository.update(document, update_data)
            
            if employee:
                return {
                    "success": True,
                    "message": "Employee deactivated successfully"
                }
            
            return {
                "success": False,
                "message": "Error deactivating employee"
            }
        except Exception as e:
            logger.error(f"Error in delete_employee: {e}")
            return {
                "success": False,
                "message": f"Error deleting employee: {str(e)}"
            }
    
    def validate_employee(self, document: str) -> Dict:
        """Validate if employee exists and is active (for SAGA)"""
        try:
            employee = self.repository.find_by_document(document)
            
            if employee:
                return {
                    "document": document,
                    "exists": True,
                    "active": employee.is_active(),
                    "name": employee.full_name,
                    "errorMessage": "" if employee.is_active() else "Employee is inactive"
                }
            
            return {
                "document": document,
                "exists": False,
                "active": False,
                "name": "",
                "errorMessage": "Employee not found"
            }
        except Exception as e:
            logger.error(f"Error in validate_employee: {e}")
            return {
                "document": document,
                "exists": False,
                "active": False,
                "name": "",
                "errorMessage": f"Error validating employee: {str(e)}"
            }
