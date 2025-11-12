import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'postgres')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'accesscontroldb')
    DB_USER = os.getenv('DB_USER', 'admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin123')
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(',')
    KAFKA_TOPIC_CHECKIN_REQUEST = os.getenv('KAFKA_TOPIC_CHECKIN_REQUEST', 'access-checkin-request')
    KAFKA_TOPIC_CHECKOUT_REQUEST = os.getenv('KAFKA_TOPIC_CHECKOUT_REQUEST', 'access-checkout-request')
    KAFKA_TOPIC_ALERT_NOTIFICATION = os.getenv('KAFKA_TOPIC_ALERT_NOTIFICATION', 'alert-notification')
    
    # Service
    SERVICE_PORT = int(os.getenv('SERVICE_PORT', 8083))
    
    # SAGA Orchestrator
    SAGA_ORCHESTRATOR_URL = os.getenv('SAGA_ORCHESTRATOR_URL', 'http://saga-orchestrator:8085')
