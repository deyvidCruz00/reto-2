from domain.ports.access_ports import AccessUseCasePort
from kafka import KafkaConsumer
from config import Config
from threading import Thread
import json
import logging

logger = logging.getLogger(__name__)


class KafkaAccessConsumer:
    """Kafka consumer for access registration requests from saga orchestrator"""
    
    def __init__(self, access_use_case: AccessUseCasePort):
        self.access_use_case = access_use_case
        self.consumer = None
        self.consumer_thread = None

    def start_consumer(self):
        """Start Kafka consumer for access registration requests"""
        
        def consume():
            try:
                # Subscribe to both check-in and check-out topics
                topics = [
                    Config.KAFKA_TOPIC_ACCESS_REGISTRATION_REQUEST,
                    Config.KAFKA_TOPIC_ACCESS_CHECKOUT_REQUEST
                ]
                
                self.consumer = KafkaConsumer(
                    *topics,
                    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    group_id='access-control-service-group',
                    auto_offset_reset='latest'
                )
                
                logger.info("Kafka consumer started for access registration requests")
                
                for message in self.consumer:
                    try:
                        request = message.value
                        logger.info(f"Received access registration request: {request}")
                        
                        saga_id = request.get('sagaId')
                        employee_id = request.get('employeeId')
                        employee_name = request.get('employeeName', '')
                        action = request.get('action', 'CHECK_IN')
                        
                        if saga_id and employee_id:
                            if action == 'CHECK_IN':
                                self.access_use_case.process_checkin_request(
                                    saga_id, employee_id, employee_name
                                )
                            elif action == 'CHECK_OUT':
                                self.access_use_case.process_checkout_request(
                                    saga_id, employee_id, employee_name
                                )
                            else:
                                logger.error(f"Unknown action: {action}")
                        else:
                            logger.error(f"Invalid request format: {request}")
                        
                    except Exception as e:
                        logger.error(f"Error processing access registration request: {e}")
                        
            except Exception as e:
                logger.error(f"Error in Kafka consumer: {e}")
        
        # Start consumer in background thread
        self.consumer_thread = Thread(target=consume, daemon=True)
        self.consumer_thread.start()
        logger.info("Kafka consumer thread started")

    def close(self):
        """Close Kafka consumer connection"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed")
