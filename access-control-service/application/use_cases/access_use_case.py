from domain.ports.access_ports import (
    AccessRepositoryPort,
    EventPublisherPort,
    AccessUseCasePort
)
from domain.entities.access import Access
from application.dto.access_dto import AccessRecordResponseDTO
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class AccessUseCase(AccessUseCasePort):
    """Use case implementation for access control business logic"""
    
    def __init__(
        self,
        repository: AccessRepositoryPort,
        event_publisher: EventPublisherPort
    ):
        self.repository = repository
        self.event_publisher = event_publisher

    def user_checkin(self, employee_id: str) -> Dict:
        """
        Register user check-in
        
        Business rules:
        - Employee cannot check-in if they have an active entry
        - Alert is published if employee attempts duplicate check-in
        """
        try:
            # Check if employee already has active entry
            if self.repository.has_active_entry(employee_id):
                # Publish alert for duplicate check-in attempt
                self.event_publisher.publish_alert(
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
            
            # Convert to DTO with camelCase
            access_dto = AccessRecordResponseDTO(
                id=str(access.id),
                employee_id=access.employee_id,
                access_datetime=access.access_datetime,
                exit_datetime=access.exit_datetime,
                duration_minutes=access.duration_minutes
            )
            
            return {
                "success": True,
                "message": "Check-in registered successfully",
                "data": access_dto.model_dump(by_alias=True, mode='json')
            }
            
        except Exception as e:
            logger.error(f"Error in user_checkin: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def user_checkout(self, employee_id: str) -> Dict:
        """
        Register user check-out
        
        Business rules:
        - Employee cannot check-out if they don't have an active entry
        - Alert is published if employee attempts to check-out without active entry
        """
        try:
            # Check if employee has active entry
            if not self.repository.has_active_entry(employee_id):
                # Publish alert for invalid check-out attempt
                self.event_publisher.publish_alert(
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
                # Convert to DTO with camelCase
                access_dto = AccessRecordResponseDTO(
                    id=str(access.id),
                    employee_id=access.employee_id,
                    access_datetime=access.access_datetime,
                    exit_datetime=access.exit_datetime,
                    duration_minutes=access.duration_minutes
                )
                
                return {
                    "success": True,
                    "message": "Check-out registered successfully",
                    "data": access_dto.model_dump(by_alias=True, mode='json')
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
        """
        Get all employees who accessed on a specific date
        
        Args:
            date_str: Date in format YYYY-MM-DD
            
        Returns:
            Dict with list of access records for the date
        """
        try:
            # Parse date
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Get all accesses for the date
            accesses = self.repository.find_by_date(target_date)
            
            # Format response with DTOs
            data = []
            for access in accesses:
                access_dto = AccessRecordResponseDTO(
                    id=str(access.id),
                    employee_id=access.employee_id,
                    access_datetime=access.access_datetime,
                    exit_datetime=access.exit_datetime,
                    duration_minutes=access.duration_minutes
                )
                data.append(access_dto.model_dump(by_alias=True, mode='json'))
            
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

    def employee_by_dates(
        self,
        employee_id: str,
        start_date_str: str,
        end_date_str: str
    ) -> Dict:
        """
        Get employee access report by date range
        
        Args:
            employee_id: Employee document ID
            start_date_str: Start date in format YYYY-MM-DD
            end_date_str: End date in format YYYY-MM-DD
            
        Returns:
            Dict with access report including total duration
        """
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
            accesses = self.repository.find_by_employee_and_date_range(
                employee_id, start_date, end_date
            )
            
            # Format response with DTOs
            data = []
            total_minutes = 0
            
            for access in accesses:
                duration = access.duration_minutes if access.duration_minutes else 0
                total_minutes += duration
                
                access_dto = AccessRecordResponseDTO(
                    id=str(access.id),
                    employee_id=access.employee_id,
                    access_datetime=access.access_datetime,
                    exit_datetime=access.exit_datetime,
                    duration_minutes=access.duration_minutes
                )
                
                data.append(access_dto.model_dump(by_alias=True, mode='json'))
            
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
    
    def get_all_active_accesses(self) -> Dict:
        """
        Get all active access records (employees currently inside)
        
        Returns:
            Dict with list of active access records
        """
        try:
            # Get all active accesses from repository
            accesses = self.repository.find_all_active()
            
            # Format response with DTOs
            data = []
            for access in accesses:
                access_dto = AccessRecordResponseDTO(
                    id=str(access.id),
                    employee_id=access.employee_id,
                    access_datetime=access.access_datetime,
                    exit_datetime=access.exit_datetime,
                    duration_minutes=access.duration_minutes
                )
                data.append(access_dto.model_dump(by_alias=True, mode='json'))
            
            return {
                "success": True,
                "message": f"Found {len(data)} active accesses",
                "count": len(data),
                "data": data
            }
            
        except Exception as e:
            logger.error(f"Error in get_all_active_accesses: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def process_checkin_request(
        self,
        saga_id: str,
        employee_id: str,
        employee_name: str
    ) -> None:
        """
        Process check-in request from saga orchestrator
        
        This is called by the Kafka consumer when a check-in request arrives.
        Publishes response back to orchestrator.
        """
        try:
            # Check if employee already has active entry
            if self.repository.has_active_entry(employee_id):
                # Publish alert
                self.event_publisher.publish_alert(
                    alert_code="EMPLOYEE_ALREADY_ENTERED",
                    description=f"Employee {employee_name} ({employee_id}) attempted to check-in with an active entry",
                    employee_id=employee_id
                )
                
                response = {
                    "sagaId": saga_id,
                    "success": False,
                    "accessId": None,
                    "errorMessage": "Employee already has an active entry"
                }
                self.event_publisher.publish_access_registration_response(response)
                return
            
            # Create check-in record
            access = self.repository.create_checkin(employee_id)
            
            response = {
                "sagaId": saga_id,
                "success": True,
                "accessId": str(access.id),
                "errorMessage": None
            }
            self.event_publisher.publish_access_registration_response(response)
            
        except Exception as e:
            logger.error(f"Error processing check-in: {e}")
            self._send_error_response(saga_id, str(e))

    def process_checkout_request(
        self,
        saga_id: str,
        employee_id: str,
        employee_name: str
    ) -> None:
        """
        Process check-out request from saga orchestrator
        
        This is called by the Kafka consumer when a check-out request arrives.
        Publishes response back to orchestrator.
        """
        try:
            # Check if employee has active entry
            if not self.repository.has_active_entry(employee_id):
                # Publish alert
                self.event_publisher.publish_alert(
                    alert_code="EMPLOYEE_NO_ACTIVE_ENTRY",
                    description=f"Employee {employee_name} ({employee_id}) attempted to check-out without an active entry",
                    employee_id=employee_id
                )
                
                response = {
                    "sagaId": saga_id,
                    "success": False,
                    "accessId": None,
                    "errorMessage": "Employee doesn't have an active entry"
                }
                self.event_publisher.publish_access_registration_response(response)
                return
            
            # Create check-out record
            access = self.repository.create_checkout(employee_id)
            
            if access:
                response = {
                    "sagaId": saga_id,
                    "success": True,
                    "accessId": str(access.id),
                    "errorMessage": None
                }
                self.event_publisher.publish_access_registration_response(response)
            else:
                self._send_error_response(saga_id, "Error registering check-out")
            
        except Exception as e:
            logger.error(f"Error processing check-out: {e}")
            self._send_error_response(saga_id, str(e))

    def _send_error_response(self, saga_id: str, error_message: str) -> None:
        """Send error response to saga orchestrator"""
        response = {
            "sagaId": saga_id,
            "success": False,
            "accessId": None,
            "errorMessage": error_message
        }
        self.event_publisher.publish_access_registration_response(response)
