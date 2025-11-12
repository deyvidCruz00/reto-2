import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://admin:admin123@mongodb:27017/employeedb?authSource=admin')
    MONGO_DB = os.getenv('MONGO_DB', 'employeedb')
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(',')
    KAFKA_TOPIC_EMPLOYEE_CREATED = os.getenv('KAFKA_TOPIC_EMPLOYEE_CREATED', 'employee-created')
    KAFKA_TOPIC_EMPLOYEE_UPDATED = os.getenv('KAFKA_TOPIC_EMPLOYEE_UPDATED', 'employee-updated')
    KAFKA_TOPIC_EMPLOYEE_VALIDATION_REQUEST = os.getenv('KAFKA_TOPIC_EMPLOYEE_VALIDATION_REQUEST', 'employee-validation-request')
    KAFKA_TOPIC_EMPLOYEE_VALIDATION_RESPONSE = os.getenv('KAFKA_TOPIC_EMPLOYEE_VALIDATION_RESPONSE', 'employee-validation-response')
    
    # Service
    SERVICE_PORT = int(os.getenv('SERVICE_PORT', 8082))
