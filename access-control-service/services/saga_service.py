from kafka import KafkaProducer
from kafka.errors import KafkaError
from config import Config
import json
import logging
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

class SagaService:
    def __init__(self):
        self.producer = None
        self._init_producer()

    def _init_producer(self):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                acks='all',
                retries=3
            )
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Kafka producer: {e}")

    def start_checkin_saga(self, employee_id: str) -> dict:
        """Start check-in SAGA orchestration"""
        try:
            saga_request = {
                "sagaType": "CHECK_IN",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "employeeId": employee_id
                }
            }
            
            # Publish to Kafka
            future = self.producer.send(
                Config.KAFKA_TOPIC_CHECKIN_REQUEST,
                value=saga_request
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Check-in SAGA started for employee: {employee_id}")
            
            return {
                "success": True,
                "sagaId": record_metadata.timestamp,
                "message": "Check-in SAGA initiated"
            }
            
        except Exception as e:
            logger.error(f"Error starting check-in SAGA: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def start_checkout_saga(self, employee_id: str) -> dict:
        """Start check-out SAGA orchestration"""
        try:
            saga_request = {
                "sagaType": "CHECK_OUT",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "employeeId": employee_id
                }
            }
            
            # Publish to Kafka
            future = self.producer.send(
                Config.KAFKA_TOPIC_CHECKOUT_REQUEST,
                value=saga_request
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Check-out SAGA started for employee: {employee_id}")
            
            return {
                "success": True,
                "sagaId": record_metadata.timestamp,
                "message": "Check-out SAGA initiated"
            }
            
        except Exception as e:
            logger.error(f"Error starting check-out SAGA: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

    def publish_alert(self, alert_code: str, description: str, employee_id: str = None):
        """Publish alert to Kafka"""
        try:
            alert = {
                "code": alert_code,
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
                "employee_id": employee_id,
                "severity": "WARNING"
            }
            
            future = self.producer.send(
                Config.KAFKA_TOPIC_ALERT_NOTIFICATION,
                value=alert
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Alert published: {alert_code}")
            
        except Exception as e:
            logger.error(f"Error publishing alert: {e}")

    def close(self):
        """Close Kafka connections"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
