from flask import Blueprint, request, jsonify
from services.access_service import AccessService
import logging

logger = logging.getLogger(__name__)

access_bp = Blueprint('access', __name__, url_prefix='/access')
access_service = AccessService()

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
        description: Employee already has active entry
    """
    try:
        data = request.get_json()
        
        if 'employeeId' not in data:
            return jsonify({
                "success": False,
                "message": "employeeId is required"
            }), 400
        
        employee_id = data['employeeId']
        result = access_service.user_checkin(employee_id)
        
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
        description: Employee doesn't have active entry
    """
    try:
        data = request.get_json()
        
        if 'employeeId' not in data:
            return jsonify({
                "success": False,
                "message": "employeeId is required"
            }), 400
        
        employee_id = data['employeeId']
        result = access_service.user_checkout(employee_id)
        
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
        
        if not date:
            return jsonify({
                "success": False,
                "message": "date parameter is required (format: YYYY-MM-DD)"
            }), 400
        
        result = access_service.all_employees_by_date(date)
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
        
        if not all([employee_id, start_date, end_date]):
            return jsonify({
                "success": False,
                "message": "employeeId, startDate, and endDate parameters are required (format: YYYY-MM-DD)"
            }), 400
        
        result = access_service.employee_by_dates(employee_id, start_date, end_date)
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
