"""
Kafka Event Publisher Adapter - Infrastructure Layer
"""
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from config import Config
from domain.entities.employee import Employee
from domain.ports.employee_ports import EventPublisherPort
import json
import logging
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)


class KafkaEventPublisher(EventPublisherPort):
    """Kafka implementation of Event Publisher"""
    
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
    
    def publish_employee_created(self, employee: Employee) -> None:
        """Publish employee created event"""
        try:
            event = {
                "event_type": "EMPLOYEE_CREATED",
                "timestamp": datetime.utcnow().isoformat(),
                "data": employee.model_dump()
            }
            
            future = self.producer.send(
                Config.KAFKA_TOPIC_EMPLOYEE_CREATED,
                value=event
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Employee created event published: {employee.document}")
            
        except KafkaError as e:
            logger.error(f"Error publishing employee created event: {e}")
        except Exception as e:
            logger.error(f"Unexpected error publishing event: {e}")
    
    def publish_employee_updated(self, employee: Employee) -> None:
        """Publish employee updated event"""
        try:
            event = {
                "event_type": "EMPLOYEE_UPDATED",
                "timestamp": datetime.utcnow().isoformat(),
                "data": employee.model_dump()
            }
            
            future = self.producer.send(
                Config.KAFKA_TOPIC_EMPLOYEE_UPDATED,
                value=event
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Employee updated event published: {employee.document}")
            
        except KafkaError as e:
            logger.error(f"Error publishing employee updated event: {e}")
        except Exception as e:
            logger.error(f"Unexpected error publishing event: {e}")
    
    def publish_employee_validation_response(self, validation_result: dict) -> None:
        """Publish employee validation response (for SAGA)"""
        try:
            # Format response to match saga orchestrator DTO
            response = {
                "sagaId": validation_result.get('sagaId'),
                "isValid": validation_result.get('exists', False) and validation_result.get('active', False),
                "employeeName": validation_result.get('name', ''),
                "errorMessage": validation_result.get('errorMessage', '')
            }
            
            future = self.producer.send(
                Config.KAFKA_TOPIC_EMPLOYEE_VALIDATION_RESPONSE,
                value=response
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Employee validation response published: {response}")
            
        except KafkaError as e:
            logger.error(f"Error publishing validation response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error publishing validation response: {e}")
    
    def close(self):
        """Close Kafka connections"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
