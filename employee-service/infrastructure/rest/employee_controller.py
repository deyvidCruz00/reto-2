"""
Employee REST Controller - Infrastructure Layer
"""
from flask import Blueprint, request, jsonify
from domain.ports.employee_ports import EmployeeUseCasePort
import logging

logger = logging.getLogger(__name__)


def create_employee_blueprint(employee_use_case: EmployeeUseCasePort) -> Blueprint:
    """Factory function to create employee blueprint with dependency injection"""
    
    # Create blueprint without url_prefix to handle both REST and legacy routes
    employee_bp = Blueprint('employee', __name__)
    
    # ===================================================================
    # RESTful Routes (preferred)
    # ===================================================================
    
    @employee_bp.route('/employees', methods=['POST'])
    def create_employee_rest():
        """Create a new employee (REST)"""
        return _create_employee()
    
    @employee_bp.route('/employees', methods=['GET'])
    def get_all_employees_rest():
        """Get all employees (REST)"""
        return _get_all_employees()
    
    @employee_bp.route('/employees/<document>', methods=['GET'])
    def get_employee_by_document_rest(document: str):
        """Get employee by document (REST)"""
        return _get_employee_by_document(document)
    
    @employee_bp.route('/employees', methods=['PUT'])
    def update_employee_rest():
        """Update an existing employee (REST)"""
        return _update_employee()
    
    @employee_bp.route('/employees/<document>', methods=['DELETE'])
    def delete_employee_rest(document: str):
        """Delete an employee (REST)"""
        return _delete_employee(document)
    
    # ===================================================================
    # Legacy Routes (for backward compatibility with frontend)
    # ===================================================================
    
    @employee_bp.route('/findallemployees', methods=['GET'])
    def findallemployees():
        """Get all employees (legacy route)"""
        return _get_all_employees()
    
    @employee_bp.route('/createemployee', methods=['POST'])
    def createemployee():
        """Create a new employee (legacy route)"""
        return _create_employee()
    
    @employee_bp.route('/updateemployee', methods=['PUT'])
    def updateemployee():
        """Update an existing employee (legacy route)"""
        return _update_employee()
    
    @employee_bp.route('/disableemployee/<document>', methods=['PUT', 'DELETE'])
    def disableemployee(document: str):
        """Disable/delete an employee (legacy route)"""
        return _delete_employee(document)
    
    @employee_bp.route('/enableemployee/<document>', methods=['PUT'])
    def enableemployee(document: str):
        """Enable/activate an employee (legacy route)"""
        return _activate_employee(document)
    
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
    
    # ===================================================================
    # Internal helper functions (business logic)
    # ===================================================================
    # Internal helper functions (business logic)
    # ===================================================================
    
    def _create_employee():
        """Internal: Create a new employee"""
        try:
            data = request.get_json()
            logger.info(f"Received create employee request with data: {data}")
            
            # Normalize field names (support both camelCase and lowercase)
            normalized_data = {}
            
            # Map camelCase to lowercase
            field_mapping = {
                'firstName': 'firstname',
                'firstname': 'firstname',
                'lastName': 'lastname',
                'lastname': 'lastname',
                'document': 'document',
                'documentNumber': 'document',
                'email': 'email',
                'phone': 'phone',
                'phoneNumber': 'phone',
                'status': 'status'
            }
            
            for key, value in data.items():
                normalized_key = field_mapping.get(key, key.lower())
                normalized_data[normalized_key] = value
            
            logger.info(f"Normalized data: {normalized_data}")
            
            # Validate required fields
            required_fields = ['document', 'firstname', 'lastname', 'email', 'phone']
            missing_fields = [field for field in required_fields if field not in normalized_data]
            
            if missing_fields:
                logger.error(f"Missing required fields: {missing_fields}. Received data: {data}")
                return jsonify({
                    "success": False,
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                }), 400
            
            result = employee_use_case.create_employee(normalized_data)
            
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
    
    def _get_all_employees():
        """Internal: Get all employees"""
        try:
            result = employee_use_case.find_all_employees()
            return jsonify(result), 200
        except Exception as e:
            logger.error(f"Error in get_all_employees endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    def _get_employee_by_document(document: str):
        """Internal: Get employee by document"""
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
    
    def _update_employee():
        """Internal: Update an existing employee"""
        try:
            data = request.get_json()
            logger.info(f"Received update employee request with data: {data}")
            
            # Normalize field names (support both camelCase and lowercase)
            normalized_data = {}
            
            # Map camelCase to lowercase
            field_mapping = {
                'firstName': 'firstname',
                'firstname': 'firstname',
                'lastName': 'lastname',
                'lastname': 'lastname',
                'document': 'document',
                'documentNumber': 'document',
                'email': 'email',
                'phone': 'phone',
                'phoneNumber': 'phone',
                'status': 'status'
            }
            
            for key, value in data.items():
                normalized_key = field_mapping.get(key, key.lower())
                normalized_data[normalized_key] = value
            
            logger.info(f"Normalized data: {normalized_data}")
            
            if 'document' not in normalized_data:
                return jsonify({
                    "success": False,
                    "message": "Document is required"
                }), 400
            
            result = employee_use_case.update_employee(normalized_data)
            
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
    
    def _delete_employee(document: str):
        """Internal: Delete an employee (soft delete)"""
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
    
    def _activate_employee(document: str):
        """Internal: Activate an employee"""
        try:
            result = employee_use_case.activate_employee(document)
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
        except Exception as e:
            logger.error(f"Error in activate_employee endpoint: {e}")
            return jsonify({
                "success": False,
                "message": f"Error: {str(e)}"
            }), 500
    
    return employee_bp
