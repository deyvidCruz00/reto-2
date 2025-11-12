from flask import Blueprint, request, jsonify
from services.employee_service import EmployeeService
from models.employee import EmployeeCreate
import logging

logger = logging.getLogger(__name__)

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')
employee_service = EmployeeService()

@employee_bp.route('/createemployee', methods=['POST'])
def create_employee():
    """
    Create a new employee
    ---
    tags:
      - Employee
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - document
            - firstname
            - lastname
            - email
            - phone
          properties:
            document:
              type: string
              example: "1234567890"
            firstname:
              type: string
              example: "Juan"
            lastname:
              type: string
              example: "Pérez"
            email:
              type: string
              example: "juan.perez@example.com"
            phone:
              type: string
              example: "3001234567"
            status:
              type: boolean
              default: true
    responses:
      201:
        description: Employee created successfully
      400:
        description: Invalid input or employee already exists
    """
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
        
        # Create employee
        employee_data = EmployeeCreate(**data)
        result = employee_service.create_employee(employee_data)
        
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

@employee_bp.route('/updateemployee', methods=['PUT'])
def update_employee():
    """
    Update an existing employee
    ---
    tags:
      - Employee
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - document
          properties:
            document:
              type: string
              example: "1234567890"
            firstname:
              type: string
              example: "Juan Carlos"
            lastname:
              type: string
              example: "Pérez García"
            email:
              type: string
              example: "juancarlos.perez@example.com"
            phone:
              type: string
              example: "3009876543"
            status:
              type: boolean
    responses:
      200:
        description: Employee updated successfully
      404:
        description: Employee not found
    """
    try:
        data = request.get_json()
        
        if 'document' not in data:
            return jsonify({
                "success": False,
                "message": "Document is required"
            }), 400
        
        result = employee_service.update_employee(data)
        
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

@employee_bp.route('/findallemployees', methods=['GET'])
def find_all_employees():
    """
    Get all employees
    ---
    tags:
      - Employee
    responses:
      200:
        description: List of all employees
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            data:
              type: array
              items:
                type: object
            count:
              type: integer
    """
    try:
        result = employee_service.find_all_employees()
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in find_all_employees endpoint: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "data": []
        }), 500

@employee_bp.route('/disableemployee/<document>', methods=['PUT'])
def disable_employee(document):
    """
    Disable an employee (set status to False)
    ---
    tags:
      - Employee
    parameters:
      - in: path
        name: document
        type: string
        required: true
        description: Employee document ID
    responses:
      200:
        description: Employee disabled successfully
      404:
        description: Employee not found
    """
    try:
        result = employee_service.disable_employee(document)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        logger.error(f"Error in disable_employee endpoint: {e}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@employee_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "UP",
        "service": "employee-service"
    }), 200
