from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers.access_controller import access_bp
from database.postgres import database
from config import Config
from services.access_service import AccessService
from services.saga_service import SagaService
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
        session = database.get_session()
        session.execute("SELECT 1")
        session.close()
        
        return jsonify({
            "status": "UP",
            "service": "access-control-service",
            "database": "connected"
        }), 200
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
        
        # Initialize services
        access_service = AccessService()
        saga_service = SagaService()
        
        # Start Kafka consumer for saga orchestrator requests
        logger.info("Starting Kafka consumer for saga orchestrator requests...")
        saga_service.start_consumer(access_service)
        
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
        database.close()
