"""
MongoDB Repository Adapter - Infrastructure Layer
"""
from datetime import datetime
from typing import List, Optional, Dict
import logging

from domain.ports.employee_ports import EmployeeRepositoryPort
from domain.entities.employee import Employee
from infrastructure.database.mongodb import mongodb

logger = logging.getLogger(__name__)


class MongoDBEmployeeRepository(EmployeeRepositoryPort):
    """MongoDB implementation of Employee Repository"""
    
    def __init__(self):
        self.collection = mongodb.get_collection('employee')
    
    def create(self, employee_data: Dict) -> Employee:
        """Create a new employee"""
        try:
            employee_dict = employee_data.copy()
            employee_dict['created_at'] = datetime.utcnow()
            employee_dict['updated_at'] = datetime.utcnow()
            employee_dict['_id'] = employee_dict['document']  # Use document as _id
            
            self.collection.insert_one(employee_dict)
            logger.info(f"Employee created: {employee_data['document']}")
            
            employee_dict.pop('_id', None)
            return Employee(**employee_dict)
        except Exception as e:
            logger.error(f"Error creating employee: {e}")
            raise
    
    def find_by_document(self, document: str) -> Optional[Employee]:
        """Find employee by document"""
        try:
            employee_dict = self.collection.find_one({"document": document})
            if employee_dict:
                employee_dict.pop('_id', None)  # Remove MongoDB _id
                # Ensure phone field has at least 7 characters, pad if necessary
                if 'phone' in employee_dict and len(str(employee_dict['phone'])) < 7:
                    employee_dict['phone'] = str(employee_dict['phone']).ljust(7, '0')
                    logger.warning(f"Padded phone for employee {document}: {employee_dict['phone']}")
                return Employee(**employee_dict)
            return None
        except Exception as e:
            logger.error(f"Error finding employee by document: {e}")
            return None
    
    def find_all(self) -> List[Employee]:
        """Find all employees"""
        try:
            employees = []
            for emp_dict in self.collection.find():
                try:
                    emp_dict.pop('_id', None)
                    # Ensure phone field has at least 7 characters, pad if necessary
                    if 'phone' in emp_dict and len(str(emp_dict['phone'])) < 7:
                        emp_dict['phone'] = str(emp_dict['phone']).ljust(7, '0')
                        logger.warning(f"Padded phone for employee {emp_dict.get('document', 'unknown')}: {emp_dict['phone']}")
                    employees.append(Employee(**emp_dict))
                except Exception as e:
                    logger.warning(f"Skipping invalid employee record: {e}. Data: {emp_dict}")
                    continue
            logger.info(f"Found {len(employees)} employees")
            return employees
        except Exception as e:
            logger.error(f"Error finding all employees: {e}")
            return []
    
    def update(self, document: str, employee_data: Dict) -> Optional[Employee]:
        """Update an employee"""
        try:
            # Get only fields that are not None
            update_data = {k: v for k, v in employee_data.items() if v is not None}
            
            if not update_data:
                return self.find_by_document(document)
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"document": document},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Employee updated: {document}")
                return self.find_by_document(document)
            
            return None
        except Exception as e:
            logger.error(f"Error updating employee: {e}")
            raise
    
    def delete(self, document: str) -> bool:
        """Delete an employee (soft delete - set status to False)"""
        try:
            result = self.collection.update_one(
                {"document": document},
                {"$set": {"status": False, "updated_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Employee deleted (soft): {document}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting employee: {e}")
            return False
    
    def exists(self, document: str) -> bool:
        """Check if employee exists"""
        return self.collection.count_documents({"document": document}) > 0
    
    def is_active(self, document: str) -> bool:
        """Check if employee is active"""
        employee = self.find_by_document(document)
        return employee.status if employee else False
