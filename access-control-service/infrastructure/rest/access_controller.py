from flask import Blueprint, request, jsonify
from domain.ports.access_ports import AccessUseCasePort
from application.dto.access_dto import (
    CheckInRequestDTO,
    CheckOutRequestDTO,
    DateQueryDTO,
    DateRangeQueryDTO
)
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


def create_access_blueprint(access_use_case: AccessUseCasePort) -> Blueprint:
    """
    Factory function to create access control blueprint with dependency injection
    
    Args:
        access_use_case: Access use case implementation
        
    Returns:
        Blueprint: Flask blueprint with all access control routes
    """
    access_bp = Blueprint('access', __name__, url_prefix='/access')

    @access_bp.route('/usercheckin', methods=['POST'])
    def user_checkin():
        """
        Register employee check-in
        ---
        tags:
          - Access Control
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - employeeId
              properties:
                employeeId:
                  type: string
                  example: "1234567890"
        responses:
          201:
            description: Check-in registered successfully
          400:
            description: Employee already has active entry or validation error
        """
        try:
            data = request.get_json()
            
            # Validate request with DTO
            try:
                checkin_dto = CheckInRequestDTO(**data)
            except ValidationError as e:
                return jsonify({
                    "success": False,
                    "message": "Validation error",
                    "errors": e.errors()
                }), 400
            
            # Execute use case
            result = access_use_case.user_checkin(checkin_dto.employee_id)
            
            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error in user_checkin endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

    @access_bp.route('/usercheckout', methods=['POST'])
    def user_checkout():
        """
        Register employee check-out
        ---
        tags:
          - Access Control
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - employeeId
              properties:
                employeeId:
                  type: string
                  example: "1234567890"
        responses:
          200:
            description: Check-out registered successfully
          400:
            description: Employee doesn't have active entry or validation error
        """
        try:
            data = request.get_json()
            
            # Validate request with DTO
            try:
                checkout_dto = CheckOutRequestDTO(**data)
            except ValidationError as e:
                return jsonify({
                    "success": False,
                    "message": "Validation error",
                    "errors": e.errors()
                }), 400
            
            # Execute use case
            result = access_use_case.user_checkout(checkout_dto.employee_id)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error in user_checkout endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

    @access_bp.route('/allemployeesbydate', methods=['GET'])
    def all_employees_by_date():
        """
        Get all employees who accessed on a specific date
        ---
        tags:
          - Access Control Reports
        parameters:
          - in: query
            name: date
            type: string
            required: true
            description: Date in format YYYY-MM-DD
            example: "2024-11-12"
        responses:
          200:
            description: List of employees with access on the specified date
        """
        try:
            date = request.args.get('date')
            
            # Validate query parameter with DTO
            try:
                date_query = DateQueryDTO(date=date)
            except ValidationError as e:
                return jsonify({
                    "success": False,
                    "message": "Validation error",
                    "errors": e.errors()
                }), 400
            
            # Execute use case
            result = access_use_case.all_employees_by_date(date_query.date)
            return jsonify(result), 200
                
        except Exception as e:
            logger.error(f"Error in all_employees_by_date endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

    @access_bp.route('/employeebydates', methods=['GET'])
    def employee_by_dates():
        """
        Get employee access report by date range
        ---
        tags:
          - Access Control Reports
        parameters:
          - in: query
            name: employeeId
            type: string
            required: true
            description: Employee document ID
          - in: query
            name: startDate
            type: string
            required: true
            description: Start date in format YYYY-MM-DD
          - in: query
            name: endDate
            type: string
            required: true
            description: End date in format YYYY-MM-DD
        responses:
          200:
            description: Employee access report for date range
        """
        try:
            employee_id = request.args.get('employeeId')
            start_date = request.args.get('startDate')
            end_date = request.args.get('endDate')
            
            # Validate query parameters with DTO
            try:
                date_range_query = DateRangeQueryDTO(
                    employeeId=employee_id,
                    startDate=start_date,
                    endDate=end_date
                )
            except ValidationError as e:
                return jsonify({
                    "success": False,
                    "message": "Validation error",
                    "errors": e.errors()
                }), 400
            
            # Execute use case
            result = access_use_case.employee_by_dates(
                date_range_query.employee_id,
                date_range_query.start_date,
                date_range_query.end_date
            )
            return jsonify(result), 200
                
        except Exception as e:
            logger.error(f"Error in employee_by_dates endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500

    @access_bp.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "UP",
            "service": "access-control-service"
        }), 200

    return access_bp
