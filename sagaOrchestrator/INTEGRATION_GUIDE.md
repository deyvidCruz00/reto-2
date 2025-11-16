# Guía de Integración - Servicios con Saga Orchestrator

Esta guía explica cómo los servicios `employee-service` y `access-control-service` deben integrarse con el Saga Orchestrator.

## 📋 Resumen de Integración

El Saga Orchestrator coordina transacciones distribuidas mediante eventos Kafka. Los servicios deben:
1. **Consumir** mensajes de solicitud del orchestrator
2. **Procesar** la lógica de negocio
3. **Producir** mensajes de respuesta al orchestrator

## 🔧 Employee Service - Integración

### Topics a Implementar

**CONSUME:**
- `employee-validation-request`

**PRODUCE:**
- `employee-validation-response`

### 1. Consumidor de Validación de Empleado

```python
# employee_service/services/kafka_service.py

from kafka import KafkaConsumer, KafkaProducer
import json
import logging

logger = logging.getLogger(__name__)

class EmployeeKafkaService:
    def __init__(self, bootstrap_servers, employee_repository):
        self.consumer = KafkaConsumer(
            'employee-validation-request',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='employee-service-group',
            auto_offset_reset='earliest'
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.employee_repository = employee_repository
    
    def consume_validation_requests(self):
        """Consume employee validation requests from saga orchestrator"""
        logger.info("Starting to consume employee validation requests...")
        
        for message in self.consumer:
            try:
                request = message.value
                logger.info(f"Received validation request: {request}")
                
                saga_id = request.get('sagaId')
                employee_id = request.get('employeeId')
                action = request.get('action')
                
                # Validate employee
                response = self._validate_employee(saga_id, employee_id, action)
                
                # Send response
                self._send_validation_response(response)
                
            except Exception as e:
                logger.error(f"Error processing validation request: {e}")
    
    def _validate_employee(self, saga_id, employee_id, action):
        """Validate employee exists and is active"""
        try:
            # Find employee
            employee = self.employee_repository.find_by_document(employee_id)
            
            if not employee:
                return {
                    'sagaId': saga_id,
                    'isValid': False,
                    'employeeName': None,
                    'errorMessage': 'Employee not found'
                }
            
            if employee.get('status') != 'ACTIVE':
                return {
                    'sagaId': saga_id,
                    'isValid': False,
                    'employeeName': None,
                    'errorMessage': 'Employee is not active'
                }
            
            # Employee is valid
            employee_name = f"{employee.get('firstname')} {employee.get('lastname')}"
            return {
                'sagaId': saga_id,
                'isValid': True,
                'employeeName': employee_name,
                'errorMessage': None
            }
            
        except Exception as e:
            logger.error(f"Error validating employee: {e}")
            return {
                'sagaId': saga_id,
                'isValid': False,
                'employeeName': None,
                'errorMessage': str(e)
            }
    
    def _send_validation_response(self, response):
        """Send validation response to saga orchestrator"""
        try:
            self.producer.send('employee-validation-response', value=response)
            self.producer.flush()
            logger.info(f"Sent validation response: {response}")
        except Exception as e:
            logger.error(f"Error sending validation response: {e}")
```

### 2. Iniciar el Consumidor

```python
# employee_service/app.py

from threading import Thread
from services.kafka_service import EmployeeKafkaService
from repositories.employee_repository import EmployeeRepository

# Initialize Kafka service
employee_repository = EmployeeRepository(mongo_client)
kafka_service = EmployeeKafkaService(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    employee_repository=employee_repository
)

# Start consuming in background thread
kafka_thread = Thread(target=kafka_service.consume_validation_requests, daemon=True)
kafka_thread.start()

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
```

### 3. Formato de Mensajes

**employee-validation-request:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "employeeId": "123456",
  "action": "CHECK_IN"
}
```

**employee-validation-response:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "isValid": true,
  "employeeName": "Juan Pérez",
  "errorMessage": null
}
```

## 🔧 Access Control Service - Integración

### Topics a Implementar

**CONSUME:**
- `access-checkin-request`
- `access-checkout-request`

**PRODUCE:**
- `access-checkin-response`
- `access-checkout-response`

### 1. Consumidor de Registro de Acceso

```python
# access_control_service/services/saga_service.py

from kafka import KafkaConsumer, KafkaProducer
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AccessSagaService:
    def __init__(self, bootstrap_servers, access_repository):
        self.consumer = KafkaConsumer(
            'access-checkin-request',
            'access-checkout-request',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='access-control-service-group',
            auto_offset_reset='earliest'
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.access_repository = access_repository
    
    def consume_access_requests(self):
        """Consume access registration requests from saga orchestrator"""
        logger.info("Starting to consume access requests...")
        
        for message in self.consumer:
            try:
                request = message.value
                topic = message.topic
                logger.info(f"Received request from {topic}: {request}")
                
                if topic == 'access-checkin-request':
                    response = self._handle_checkin(request)
                    self._send_response('access-checkin-response', response)
                    
                elif topic == 'access-checkout-request':
                    response = self._handle_checkout(request)
                    self._send_response('access-checkout-response', response)
                
            except Exception as e:
                logger.error(f"Error processing access request: {e}")
    
    def _handle_checkin(self, request):
        """Handle check-in request"""
        try:
            saga_id = request.get('sagaId')
            employee_id = request.get('employeeId')
            employee_name = request.get('employeeName')
            
            # Check if employee already has active entry
            active_entry = self.access_repository.find_active_entry(employee_id)
            
            if active_entry:
                return {
                    'sagaId': saga_id,
                    'success': False,
                    'accessId': None,
                    'errorMessage': 'Employee already has an active entry'
                }
            
            # Register entry
            access = {
                'employee_id': employee_id,
                'employee_name': employee_name,
                'entry_datetime': datetime.now(),
                'exit_datetime': None,
                'status': 'ACTIVE'
            }
            
            access_id = self.access_repository.create(access)
            
            return {
                'sagaId': saga_id,
                'success': True,
                'accessId': str(access_id),
                'errorMessage': None
            }
            
        except Exception as e:
            logger.error(f"Error handling check-in: {e}")
            return {
                'sagaId': saga_id,
                'success': False,
                'accessId': None,
                'errorMessage': str(e)
            }
    
    def _handle_checkout(self, request):
        """Handle check-out request"""
        try:
            saga_id = request.get('sagaId')
            employee_id = request.get('employeeId')
            
            # Find active entry
            active_entry = self.access_repository.find_active_entry(employee_id)
            
            if not active_entry:
                return {
                    'sagaId': saga_id,
                    'success': False,
                    'accessId': None,
                    'errorMessage': 'No active entry found for employee'
                }
            
            # Update exit datetime
            access_id = active_entry['id']
            self.access_repository.update_exit(access_id, datetime.now())
            
            return {
                'sagaId': saga_id,
                'success': True,
                'accessId': str(access_id),
                'errorMessage': None
            }
            
        except Exception as e:
            logger.error(f"Error handling check-out: {e}")
            return {
                'sagaId': saga_id,
                'success': False,
                'accessId': None,
                'errorMessage': str(e)
            }
    
    def _send_response(self, topic, response):
        """Send response to saga orchestrator"""
        try:
            self.producer.send(topic, value=response)
            self.producer.flush()
            logger.info(f"Sent response to {topic}: {response}")
        except Exception as e:
            logger.error(f"Error sending response: {e}")
```

### 2. Iniciar el Consumidor

```python
# access_control_service/app.py

from threading import Thread
from services.saga_service import AccessSagaService
from repositories.access_repository import AccessRepository

# Initialize Saga service
access_repository = AccessRepository(postgres_connection)
saga_service = AccessSagaService(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    access_repository=access_repository
)

# Start consuming in background thread
saga_thread = Thread(target=saga_service.consume_access_requests, daemon=True)
saga_thread.start()

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)
```

### 3. Formato de Mensajes

**access-checkin-request:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "employeeId": "123456",
  "employeeName": "Juan Pérez",
  "action": "CHECK_IN"
}
```

**access-checkin-response:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "success": true,
  "accessId": "789",
  "errorMessage": null
}
```

**access-checkout-request:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "employeeId": "123456",
  "employeeName": "Juan Pérez",
  "action": "CHECK_OUT"
}
```

**access-checkout-response:**
```json
{
  "sagaId": "550e8400-e29b-41d4-a716-446655440000",
  "success": true,
  "accessId": "789",
  "errorMessage": null
}
```

## 🔧 Alert Service - Integración

### Topics a Implementar

**CONSUME:**
- `alerts`

### Consumidor de Alertas

```java
// alert-service/src/main/java/com/uptc/alertservice/infrastructure/kafka/AlertKafkaConsumer.java

@Component
@RequiredArgsConstructor
@Slf4j
public class AlertKafkaConsumer {
    
    private final AlertService alertService;
    
    @KafkaListener(topics = "alerts", groupId = "alert-service-group")
    public void consumeAlert(String message) {
        try {
            log.info("Received alert: {}", message);
            
            ObjectMapper mapper = new ObjectMapper();
            JsonNode alert = mapper.readTree(message);
            
            String employeeId = alert.get("employeeId").asText();
            String type = alert.get("type").asText();
            String alertMessage = alert.get("message").asText();
            String severity = alert.get("severity").asText();
            
            // Process alert
            alertService.createAlert(employeeId, type, alertMessage, severity);
            
        } catch (Exception e) {
            log.error("Error processing alert", e);
        }
    }
}
```

## ✅ Checklist de Integración

### Employee Service
- [ ] Implementar EmployeeKafkaService
- [ ] Agregar consumer para `employee-validation-request`
- [ ] Agregar producer para `employee-validation-response`
- [ ] Iniciar consumer en thread background
- [ ] Probar validación exitosa
- [ ] Probar validación fallida (empleado no existe)
- [ ] Probar validación fallida (empleado inactivo)

### Access Control Service
- [ ] Implementar AccessSagaService
- [ ] Agregar consumer para `access-checkin-request`
- [ ] Agregar consumer para `access-checkout-request`
- [ ] Agregar producer para `access-checkin-response`
- [ ] Agregar producer para `access-checkout-response`
- [ ] Implementar validación de entrada activa
- [ ] Iniciar consumer en thread background
- [ ] Probar check-in exitoso
- [ ] Probar check-in fallido (entrada duplicada)
- [ ] Probar check-out exitoso
- [ ] Probar check-out fallido (sin entrada activa)

### Alert Service
- [ ] Implementar AlertKafkaConsumer
- [ ] Agregar consumer para `alerts`
- [ ] Procesar alertas tipo `EMPLOYEE_ALREADY_ENTERED`
- [ ] Almacenar alertas en base de datos
- [ ] Probar recepción de alertas

## 🧪 Pruebas de Integración

### 1. Flujo Completo Check-In Exitoso

```bash
# 1. Iniciar saga
curl -X POST http://localhost:8085/api/saga/check-in \
  -H "Content-Type: application/json" \
  -d '{"employeeId": "123456"}'

# Respuesta:
{
  "sagaId": "uuid",
  "status": "STARTED",
  ...
}

# 2. Verificar logs de employee-service (debe validar empleado)
# 3. Verificar logs de access-control-service (debe registrar entrada)
# 4. Verificar estado final de saga

curl http://localhost:8085/api/saga/{sagaId}

# Respuesta esperada:
{
  "sagaId": "uuid",
  "status": "COMPLETED",
  "accessId": "789",
  ...
}
```

### 2. Flujo Check-In con Error (Entrada Duplicada)

```bash
# 1. Empleado ya tiene entrada activa
# 2. Iniciar saga
curl -X POST http://localhost:8085/api/saga/check-in \
  -H "Content-Type: application/json" \
  -d '{"employeeId": "123456"}'

# 3. Verificar que saga falla
# 4. Verificar que se publica alerta
```

## 📚 Recursos Adicionales

- [Saga Pattern Documentation](../saga-orchestrator/README.md)
- [Architecture Diagrams](../saga-orchestrator/ARCHITECTURE.md)
- [Test Scripts](../saga-orchestrator/TEST_SCRIPTS.md)
