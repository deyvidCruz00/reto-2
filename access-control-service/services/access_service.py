from repositories.access_repository import AccessRepository
from services.saga_service import SagaService
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AccessService:
    def __init__(self):
        self.repository = AccessRepository()
        self.saga_service = SagaService()

    def user_checkin(self, employee_id: str) -> Dict:
        """Register user check-in via SAGA"""
        try:
            # Check if employee already has active entry
            if self.repository.has_active_entry(employee_id):
                # Publish alert
                self.saga_service.publish_alert(
                    alert_code="EMPLOYEE_ALREADY_ENTERED",
                    description=f"Employee {employee_id} attempted to check-in with an active entry",
                    employee_id=employee_id
                )
                
                return {
                    "success": False,
                    "message": f"Employee {employee_id} already has an active entry. Please check-out first."
                }
            
            # Create check-in record
            access = self.repository.create_checkin(employee_id)
            
            # Start SAGA orchestration (for complex validations)
            saga_result = self.saga_service.start_checkin_saga(employee_id)
            
            return {
                "success": True,
                "message": "Check-in registered successfully",
                "data": access.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error in user_checkin: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def user_checkout(self, employee_id: str) -> Dict:
        """Register user check-out via SAGA"""
        try:
            # Check if employee has active entry
            if not self.repository.has_active_entry(employee_id):
                # Publish alert
                self.saga_service.publish_alert(
                    alert_code="EMPLOYEE_ALREADY_LEFT",
                    description=f"Employee {employee_id} attempted to check-out without an active entry",
                    employee_id=employee_id
                )
                
                return {
                    "success": False,
                    "message": f"Employee {employee_id} doesn't have an active entry. Please check-in first."
                }
            
            # Create check-out record
            access = self.repository.create_checkout(employee_id)
            
            if access:
                # Start SAGA orchestration (for complex validations)
                saga_result = self.saga_service.start_checkout_saga(employee_id)
                
                return {
                    "success": True,
                    "message": "Check-out registered successfully",
                    "data": access.to_dict()
                }
            
            return {
                "success": False,
                "message": "Error registering check-out"
            }
            
        except Exception as e:
            logger.error(f"Error in user_checkout: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def all_employees_by_date(self, date_str: str) -> Dict:
        """Get all employees who accessed on a specific date"""
        try:
            # Parse date
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Get all accesses for the date
            accesses = self.repository.find_by_date(target_date)
            
            # Format response
            data = []
            for access in accesses:
                data.append({
                    "employee_id": access.employee_id,
                    "access_datetime": access.access_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "exit_datetime": access.exit_datetime.strftime("%Y-%m-%d %H:%M:%S") if access.exit_datetime else "Still inside",
                    "duration_minutes": access.duration_minutes if access.duration_minutes else "N/A"
                })
            
            return {
                "success": True,
                "message": f"Found {len(data)} accesses for date {date_str}",
                "date": date_str,
                "count": len(data),
                "data": data
            }
            
        except ValueError as e:
            return {
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD"
            }
        except Exception as e:
            logger.error(f"Error in all_employees_by_date: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def employee_by_dates(self, employee_id: str, start_date_str: str, end_date_str: str) -> Dict:
        """Get employee access report by date range"""
        try:
            # Parse dates
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            # Validate date range
            if start_date > end_date:
                return {
                    "success": False,
                    "message": "Start date cannot be after end date"
                }
            
            # Get accesses for employee in date range
            accesses = self.repository.find_by_employee_and_date_range(employee_id, start_date, end_date)
            
            # Format response
            data = []
            total_minutes = 0
            
            for access in accesses:
                duration = access.duration_minutes if access.duration_minutes else 0
                total_minutes += duration
                
                data.append({
                    "date": access.access_datetime.strftime("%Y-%m-%d"),
                    "access_time": access.access_datetime.strftime("%H:%M:%S"),
                    "exit_time": access.exit_datetime.strftime("%H:%M:%S") if access.exit_datetime else "Still inside",
                    "duration_minutes": access.duration_minutes if access.duration_minutes else "N/A",
                    "duration_hours": f"{duration // 60}h {duration % 60}m" if access.duration_minutes else "N/A"
                })
            
            return {
                "success": True,
                "message": f"Found {len(data)} accesses for employee {employee_id}",
                "employee_id": employee_id,
                "start_date": start_date_str,
                "end_date": end_date_str,
                "total_accesses": len(data),
                "total_duration_hours": f"{total_minutes // 60}h {total_minutes % 60}m",
                "data": data
            }
            
        except ValueError as e:
            return {
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD"
            }
        except Exception as e:
            logger.error(f"Error in employee_by_dates: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }
