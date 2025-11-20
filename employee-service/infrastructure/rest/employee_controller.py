"""
Employee REST Controller - Infrastructure Layer
"""
from flask import Blueprint, request, jsonify
from domain.ports.employee_ports import EmployeeUseCasePort
import logging

logger = logging.getLogger(__name__)


def create_employee_blueprint(employee_use_case: EmployeeUseCasePort) -> Blueprint:
    """Factory function to create employee blueprint with dependency injection"""
    
    employee_bp = Blueprint('employee', __name__, url_prefix='/employees')
    
    @employee_bp.route('', methods=['POST'])
    def create_employee():
        """Create a new employee"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['document', 'firstname', 'lastname', 'email', 'phone']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        "success": False,
                        "message": f"Missing required field: {field}"
                    }), 400
            
            result = employee_use_case.create_employee(data)
            
            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Error in create_employee endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @employee_bp.route('', methods=['GET'])
    def get_all_employees():
        """Get all employees"""
        try:
            result = employee_use_case.find_all_employees()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error in get_all_employees endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @employee_bp.route('/<document>', methods=['GET'])
    def get_employee_by_document(document: str):
        """Get employee by document"""
        try:
            result = employee_use_case.find_employee_by_document(document)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
        except Exception as e:
            logger.error(f"Error in get_employee_by_document endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @employee_bp.route('', methods=['PUT'])
    def update_employee():
        """Update an existing employee"""
        try:
            data = request.get_json()
            
            if 'document' not in data:
                return jsonify({
                    "success": False,
                    "message": "Document is required"
                }), 400
            
            result = employee_use_case.update_employee(data)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            logger.error(f"Error in update_employee endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @employee_bp.route('/<document>', methods=['DELETE'])
    def delete_employee(document: str):
        """Delete an employee (soft delete)"""
        try:
            result = employee_use_case.delete_employee(document)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
        except Exception as e:
            logger.error(f"Error in delete_employee endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    @employee_bp.route('/<document>/validate', methods=['GET'])
    def validate_employee(document: str):
        """Validate employee (for testing)"""
        try:
            result = employee_use_case.validate_employee(document)
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error in validate_employee endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    return employee_bp
