from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import time

# Hexagonal Architecture imports
from infrastructure.database.mongodb import mongodb
from infrastructure.adapters.mongodb_employee_repository import MongoDBEmployeeRepository
from infrastructure.kafka.kafka_event_publisher import KafkaEventPublisher
from infrastructure.kafka.kafka_employee_validation_consumer import KafkaEmployeeValidationConsumer
from application.use_cases.employee_use_case import EmployeeUseCase
from infrastructure.rest.employee_controller import create_employee_blueprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
# CORS(app)  # Disabled - API Gateway handles CORS

# Prometheus metrics
REQUEST_COUNT = Counter(
    'employee_service_requests_total',
    'Total requests to employee service',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'employee_service_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

@app.before_request
def before_request():
    request._start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(request, '_start_time'):
        duration = time.time() - request._start_time
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown'
        ).observe(duration)
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
    
    return response

@app.route('/')
def index():
    return jsonify({
        "service": "Employee Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "create": "POST /employee/createemployee",
            "update": "PUT /employee/updateemployee",
            "list": "GET /employee/findallemployees",
            "disable": "PUT /employee/disableemployee/<document>",
            "health": "GET /employee/health"
        }
    })

@app.route('/health')
def health():
    try:
        # Test MongoDB connection
        mongodb.ping()
        return jsonify({
            "status": "UP",
            "service": "employee-service",
            "architecture": "Hexagonal",
            "database": "connected"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "DOWN",
            "service": "employee-service",
            "error": str(e)
        }), 503

# Prometheus metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Swagger/OpenAPI info
@app.route('/api-docs')
def api_docs():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Employee Service API",
            "description": "API for employee management",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "http://localhost:8082", "description": "Local server"},
            {"url": "http://employee-service:8082", "description": "Docker server"}
        ],
        "paths": {
            "/employee/createemployee": {
                "post": {"summary": "Create a new employee"}
            },
            "/employee/updateemployee": {
                "put": {"summary": "Update an existing employee"}
            },
            "/employee/findallemployees": {
                "get": {"summary": "Get all employees"}
            },
            "/employee/disableemployee/{document}": {
                "put": {"summary": "Disable an employee"}
            }
        }
    })

if __name__ == '__main__':
    try:
        # Connect to MongoDB
        logger.info("Connecting to MongoDB...")
        mongodb.connect()
        
        # Initialize dependencies after MongoDB connection
        logger.info("Initializing dependencies...")
        repository = MongoDBEmployeeRepository()
        event_publisher = KafkaEventPublisher()
        employee_use_case = EmployeeUseCase(repository, event_publisher)
        
        # Create and register blueprint
        employee_bp = create_employee_blueprint(employee_use_case)
        app.register_blueprint(employee_bp)
        
        # Start Kafka consumer for SAGA
        logger.info("Starting Kafka consumer for SAGA validation requests...")
        kafka_consumer = KafkaEmployeeValidationConsumer(employee_use_case, event_publisher)
        kafka_consumer.start_consumer()
        
        # Start Flask app
        logger.info(f"Starting Employee Service on port {Config.SERVICE_PORT}")
        app.run(
            host='0.0.0.0',
            port=Config.SERVICE_PORT,
            debug=Config.DEBUG
        )
        
    except Exception as e:
        logger.error(f"Failed to start Employee Service: {e}")
        raise
    finally:
        mongodb.close()
        if 'event_publisher' in locals():
            event_publisher.close()
