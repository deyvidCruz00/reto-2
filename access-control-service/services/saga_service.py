from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
from config import Config
import json
import logging
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)

class SagaService:
    def __init__(self):
        self.producer = None
        self.access_service = None
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

    def publish_access_registration_response(self, response: dict):
        """Publish access registration response to saga orchestrator"""
        try:
            future = self.producer.send(
                Config.KAFKA_TOPIC_ACCESS_REGISTRATION_RESPONSE,
                value=response
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Access registration response published: {response}")
            
        except KafkaError as e:
            logger.error(f"Error publishing access registration response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error publishing response: {e}")

    def publish_alert(self, alert_code: str, description: str, employee_id: str = None):
        """Publish alert to Kafka"""
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
            
        except Exception as e:
            logger.error(f"Error publishing alert: {e}")

    def start_consumer(self, access_service_instance):
        """Start Kafka consumer for access registration requests from saga orchestrator"""
        self.access_service = access_service_instance
        
        def consume():
            try:
                consumer = KafkaConsumer(
                    Config.KAFKA_TOPIC_ACCESS_REGISTRATION_REQUEST,
                    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    group_id='access-control-service-group',
                    auto_offset_reset='latest'
                )
                
                logger.info("Kafka consumer started for access registration requests")
                
                for message in consumer:
                    try:
                        request = message.value
                        logger.info(f"Received access registration request: {request}")
                        
                        saga_id = request.get('sagaId')
                        employee_id = request.get('employeeId')
                        employee_name = request.get('employeeName', '')
                        action = request.get('action', 'CHECK_IN')
                        
                        if saga_id and employee_id:
                            if action == 'CHECK_IN':
                                self._process_checkin_request(saga_id, employee_id, employee_name)
                            elif action == 'CHECK_OUT':
                                self._process_checkout_request(saga_id, employee_id, employee_name)
                            else:
                                logger.error(f"Unknown action: {action}")
                        else:
                            logger.error(f"Invalid request format: {request}")
                        
                    except Exception as e:
                        logger.error(f"Error processing access registration request: {e}")
                        if saga_id:
                            self._send_error_response(saga_id, str(e))
                        
            except Exception as e:
                logger.error(f"Error in Kafka consumer: {e}")
        
        # Start consumer in background thread
        consumer_thread = Thread(target=consume, daemon=True)
        consumer_thread.start()
        logger.info("Kafka consumer thread started")

    def _process_checkin_request(self, saga_id: str, employee_id: str, employee_name: str):
        """Process check-in request from saga"""
        try:
            # Check if employee already has active entry
            if self.access_service.repository.has_active_entry(employee_id):
                # Publish alert
                self.publish_alert(
                    alert_code="EMPLOYEE_ALREADY_ENTERED",
                    description=f"Employee {employee_name} ({employee_id}) attempted to check-in with an active entry",
                    employee_id=employee_id
                )
                
                response = {
                    "sagaId": saga_id,
                    "success": False,
                    "accessId": None,
                    "errorMessage": f"Employee already has an active entry"
                }
                self.publish_access_registration_response(response)
                return
            
            # Create check-in record
            access = self.access_service.repository.create_checkin(employee_id)
            
            response = {
                "sagaId": saga_id,
                "success": True,
                "accessId": str(access.id),
                "errorMessage": None
            }
            self.publish_access_registration_response(response)
            
        except Exception as e:
            logger.error(f"Error processing check-in: {e}")
            self._send_error_response(saga_id, str(e))

    def _process_checkout_request(self, saga_id: str, employee_id: str, employee_name: str):
        """Process check-out request from saga"""
        try:
            # Check if employee has active entry
            if not self.access_service.repository.has_active_entry(employee_id):
                # Publish alert
                self.publish_alert(
                    alert_code="EMPLOYEE_NO_ACTIVE_ENTRY",
                    description=f"Employee {employee_name} ({employee_id}) attempted to check-out without an active entry",
                    employee_id=employee_id
                )
                
                response = {
                    "sagaId": saga_id,
                    "success": False,
                    "accessId": None,
                    "errorMessage": f"Employee doesn't have an active entry"
                }
                self.publish_access_registration_response(response)
                return
            
            # Create check-out record
            access = self.access_service.repository.create_checkout(employee_id)
            
            if access:
                response = {
                    "sagaId": saga_id,
                    "success": True,
                    "accessId": str(access.id),
                    "errorMessage": None
                }
                self.publish_access_registration_response(response)
            else:
                self._send_error_response(saga_id, "Error registering check-out")
            
        except Exception as e:
            logger.error(f"Error processing check-out: {e}")
            self._send_error_response(saga_id, str(e))

    def _send_error_response(self, saga_id: str, error_message: str):
        """Send error response to saga orchestrator"""
        response = {
            "sagaId": saga_id,
            "success": False,
            "accessId": None,
            "errorMessage": error_message
        }
        self.publish_access_registration_response(response)

    def close(self):
        """Close Kafka connections"""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
