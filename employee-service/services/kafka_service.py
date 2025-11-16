from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from config import Config
from models.employee import Employee
import json
import logging
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)

class KafkaService:
    def __init__(self):
        self.producer = None
        self.consumer = None
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

    def publish_employee_created(self, employee: Employee):
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
            
            # Wait for send to complete
            record_metadata = future.get(timeout=10)
            logger.info(f"Employee created event published: {employee.document}")
            
        except KafkaError as e:
            logger.error(f"Error publishing employee created event: {e}")
        except Exception as e:
            logger.error(f"Unexpected error publishing event: {e}")

    def publish_employee_updated(self, employee: Employee):
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

    def publish_employee_validation_response(self, validation_result: dict):
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

    def start_consumer(self, employee_service):
        """Start Kafka consumer for validation requests (SAGA)"""
        def consume():
            try:
                consumer = KafkaConsumer(
                    Config.KAFKA_TOPIC_EMPLOYEE_VALIDATION_REQUEST,
                    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    group_id='employee-service-group',
                    auto_offset_reset='latest'
                )
                
                logger.info("Kafka consumer started for employee validation requests")
                
                for message in consumer:
                    try:
                        request = message.value
                        logger.info(f"Received validation request: {request}")
                        
                        # Extract data from saga orchestrator format
                        saga_id = request.get('sagaId')
                        employee_id = request.get('employeeId')
                        
                        if employee_id and saga_id:
                            # Validate employee
                            employee = employee_service.repository.find_by_document(employee_id)
                            
                            validation_result = {
                                'sagaId': saga_id,
                                'exists': employee is not None,
                                'active': employee.active if employee else False,
                                'name': f"{employee.name} {employee.lastname}" if employee else '',
                                'errorMessage': '' if employee and employee.active else 'Employee not found or inactive'
                            }
                            
                            # Publish response
                            self.publish_employee_validation_response(validation_result)
                        else:
                            logger.error(f"Invalid request format: {request}")
                        
                    except Exception as e:
                        logger.error(f"Error processing validation request: {e}")
                        # Send error response
                        if saga_id:
                            error_result = {
                                'sagaId': saga_id,
                                'exists': False,
                                'active': False,
                                'name': '',
                                'errorMessage': f"Error processing request: {str(e)}"
                            }
                            self.publish_employee_validation_response(error_result)
                        
            except Exception as e:
                logger.error(f"Error in Kafka consumer: {e}")
        
        # Start consumer in background thread
        consumer_thread = Thread(target=consume, daemon=True)
        consumer_thread.start()
        logger.info("Kafka consumer thread started")

    def close(self):
        """Close Kafka connections"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")
