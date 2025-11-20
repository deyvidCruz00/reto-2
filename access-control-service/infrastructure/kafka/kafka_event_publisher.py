from domain.ports.access_ports import EventPublisherPort
from kafka import KafkaProducer
from kafka.errors import KafkaError
from config import Config
from datetime import datetime
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)


class KafkaEventPublisher(EventPublisherPort):
    """Kafka adapter for publishing events"""
    
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
            raise

    def publish_access_registration_response(self, response: dict) -> None:
        """
        Publish access registration response to saga orchestrator
        
        Args:
            response: Response dict with sagaId, success, accessId, errorMessage
        """
        try:
            future = self.producer.send(
                Config.KAFKA_TOPIC_ACCESS_REGISTRATION_RESPONSE,
                value=response
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Access registration response published: {response}")
            
        except KafkaError as e:
            logger.error(f"Error publishing access registration response: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing response: {e}")
            raise

    def publish_alert(
        self,
        alert_code: str,
        description: str,
        employee_id: Optional[str] = None
    ) -> None:
        """
        Publish alert to Kafka
        
        Args:
            alert_code: Alert code (e.g., EMPLOYEE_ALREADY_ENTERED)
            description: Alert description
            employee_id: Optional employee ID related to the alert
        """
        try:
            alert = {
                "code": alert_code,
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
                "employeeId": employee_id,
                "severity": "WARNING"
            }
            
            future = self.producer.send(
                Config.KAFKA_TOPIC_ALERTS,
                value=alert
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Alert published: {alert_code}")
            
        except KafkaError as e:
            logger.error(f"Error publishing alert: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error publishing alert: {e}")
            raise

    def close(self):
        """Close Kafka producer connection"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
