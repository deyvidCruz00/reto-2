from repositories.employee_repository import EmployeeRepository
from models.employee import Employee, EmployeeCreate, EmployeeUpdate
from services.kafka_service import KafkaService
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class EmployeeService:
    def __init__(self):
        self.repository = EmployeeRepository()
        self.kafka_service = KafkaService()

    def create_employee(self, employee_data: EmployeeCreate) -> Dict:
        """Create a new employee"""
        try:
            # Check if employee already exists
            if self.repository.exists(employee_data.document):
                return {
                    "success": False,
                    "message": f"Employee with document {employee_data.document} already exists"
                }

            # Create employee
            employee = self.repository.create(employee_data)
            
            # Publish event to Kafka
            self.kafka_service.publish_employee_created(employee)
            
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

            # Create update object (excluding document)
            update_data = EmployeeUpdate(
                firstname=employee_data.get('firstname'),
                lastname=employee_data.get('lastname'),
                email=employee_data.get('email'),
                phone=employee_data.get('phone'),
                status=employee_data.get('status')
            )

            # Update employee
            employee = self.repository.update(document, update_data)
            
            if employee:
                # Publish event to Kafka
                self.kafka_service.publish_employee_updated(employee)
                
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
                "data": []
            }

    def disable_employee(self, document: str) -> Dict:
        """Disable an employee"""
        try:
            # Check if employee exists
            if not self.repository.exists(document):
                return {
                    "success": False,
                    "message": f"Employee with document {document} not found"
                }

            # Disable employee
            result = self.repository.disable(document)
            
            if result:
                employee = self.repository.find_by_document(document)
                # Publish event to Kafka
                self.kafka_service.publish_employee_updated(employee)
                
                return {
                    "success": True,
                    "message": f"Employee {document} disabled successfully"
                }
            
            return {
                "success": False,
                "message": "Error disabling employee"
            }
        except Exception as e:
            logger.error(f"Error in disable_employee: {e}")
            return {
                "success": False,
                "message": f"Error disabling employee: {str(e)}"
            }

    def validate_employee(self, document: str) -> Dict:
        """Validate if employee exists and is active (for SAGA)"""
        try:
            exists = self.repository.exists(document)
            active = self.repository.is_active(document) if exists else False
            
            return {
                "document": document,
                "exists": exists,
                "active": active
            }
        except Exception as e:
            logger.error(f"Error in validate_employee: {e}")
            return {
                "document": document,
                "exists": False,
                "active": False
            }
