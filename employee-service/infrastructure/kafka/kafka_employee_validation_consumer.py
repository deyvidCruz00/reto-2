"""
Kafka Consumer for SAGA - Infrastructure Layer
"""
from kafka import KafkaConsumer
from config import Config
import json
import logging
from threading import Thread

logger = logging.getLogger(__name__)


class KafkaEmployeeValidationConsumer:
    """Kafka consumer for employee validation requests from SAGA orchestrator"""
    
    def __init__(self, employee_use_case, event_publisher):
        self.employee_use_case = employee_use_case
        self.event_publisher = event_publisher
    
    def start_consumer(self):
        """Start Kafka consumer for validation requests"""
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
                            # Validate employee using use case
                            validation_result = self.employee_use_case.validate_employee(employee_id)
                            validation_result['sagaId'] = saga_id
                            
                            # Publish response
                            self.event_publisher.publish_employee_validation_response(validation_result)
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
                            self.event_publisher.publish_employee_validation_response(error_result)
                        
            except Exception as e:
                logger.error(f"Error in Kafka consumer: {e}")
        
        # Start consumer in background thread
        consumer_thread = Thread(target=consume, daemon=True)
        consumer_thread.start()
        logger.info("Kafka consumer thread started")
