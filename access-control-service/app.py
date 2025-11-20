from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import logging
import time

# Hexagonal Architecture Imports
from infrastructure.database.postgres import database
from infrastructure.adapters.postgres_access_repository import PostgresAccessRepository
from infrastructure.kafka.kafka_event_publisher import KafkaEventPublisher
from infrastructure.kafka.kafka_access_consumer import KafkaAccessConsumer
from infrastructure.rest.access_controller import create_access_blueprint
from application.use_cases.access_use_case import AccessUseCase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)

# ==============================================
# DEPENDENCY INJECTION (Hexagonal Architecture)
# ==============================================

# Infrastructure Layer - Adapters
repository = PostgresAccessRepository()
event_publisher = KafkaEventPublisher()

# Application Layer - Use Cases
access_use_case = AccessUseCase(repository, event_publisher)

# Infrastructure Layer - REST Controller (with DI)
access_bp = create_access_blueprint(access_use_case)

# Infrastructure Layer - Kafka Consumer (with DI)
kafka_consumer = KafkaAccessConsumer(access_use_case)

# ==============================================

# Prometheus metrics
REQUEST_COUNT = Counter(
    'access_service_requests_total',
    'Total requests to access control service',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'access_service_request_duration_seconds',
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
app.register_blueprint(access_bp)

# Root endpoint
@app.route('/')
def index():
    return jsonify({
        "service": "Access Control Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "checkin": "POST /access/usercheckin",
            "checkout": "POST /access/usercheckout",
            "report_by_date": "GET /access/allemployeesbydate?date=YYYY-MM-DD",
            "report_by_employee": "GET /access/employeebydates?employeeId=XXX&startDate=YYYY-MM-DD&endDate=YYYY-MM-DD",
            "health": "GET /access/health"
        }
    })

# Health endpoint
@app.route('/health')
def health():
    try:
        # Test database connection
        db_status = database.ping()
        
        return jsonify({
            "status": "UP" if db_status else "DEGRADED",
            "service": "access-control-service",
            "database": "connected" if db_status else "disconnected"
        }), 200 if db_status else 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "DOWN",
            "service": "access-control-service",
            "error": str(e)
        }), 503

# Prometheus metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    try:
        # Connect to database
        logger.info("Connecting to PostgreSQL...")
        database.connect()
        
        # Start Kafka consumer for saga orchestrator requests
        logger.info("Starting Kafka consumer for saga orchestrator requests...")
        kafka_consumer.start_consumer()
        
        # Start Flask app
        logger.info(f"Starting Access Control Service on port {Config.SERVICE_PORT}")
        app.run(
            host='0.0.0.0',
            port=Config.SERVICE_PORT,
            debug=Config.DEBUG
        )
        
    except Exception as e:
        logger.error(f"Failed to start Access Control Service: {e}")
        raise
    finally:
        # Clean up resources
        kafka_consumer.close()
        event_publisher.close()
        database.close()
