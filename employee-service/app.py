from flask import Flask, jsonify
from flask_cors import CORS
from controllers.employee_controller import employee_bp, employee_service
from database.mongodb import mongodb
from config import Config
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

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

# Middleware for metrics
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

# Register blueprints
app.register_blueprint(employee_bp)

# Root endpoint
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

# Health endpoint
@app.route('/health')
def health():
    try:
        # Test MongoDB connection
        mongodb.get_database().command('ping')
        return jsonify({
            "status": "UP",
            "service": "employee-service",
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
        
        # Start Kafka consumer in background
        logger.info("Starting Kafka consumer...")
        from services.kafka_service import KafkaService
        kafka_service = KafkaService()
        kafka_service.start_consumer(employee_service)
        
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
