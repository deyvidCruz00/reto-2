# Saga Orchestrator Service

Orquestador de Sagas para el sistema de control de acceso. Implementa el patrón Saga con orquestación centralizada para coordinar transacciones distribuidas entre microservicios.

## Arquitectura

### Patrón Saga con Orquestación
- **Orquestador centralizado**: Coordina todos los pasos de la saga
- **Persistencia de estado**: Base de datos PostgreSQL para estado de sagas
- **Comunicación asíncrona**: Kafka para mensajería entre servicios
- **Compensación automática**: Rollback de transacciones en caso de fallo
- **Timeout handling**: Manejo de timeouts (30 segundos)
- **Arquitectura hexagonal**: Separación clara entre dominio, aplicación e infraestructura

## Tecnologías

- **Spring Boot 3.2.0**
- **PostgreSQL 15** (Estado de sagas)
- **Apache Kafka** (Mensajería)
- **Spring Data JPA** (Persistencia)
- **Prometheus/Actuator** (Métricas)
- **Lombok** (Reducción de boilerplate)

## Sagas Implementadas

### 1. Check-In Saga

**Flujo:**
1. **VALIDATE_EMPLOYEE**: Valida que el empleado existe y está activo
2. **CHECK_ACTIVE_ENTRY**: Verifica que no tenga entrada activa
3. **REGISTER_ACCESS**: Registra la entrada en Access Control

**Compensaciones:**
- Si falla paso 3 (empleado ya tiene entrada): Publica alerta `EMPLOYEE_ALREADY_ENTERED`
- Si falla validación de empleado: Termina saga con error

**Topics Kafka:**
- **Produce:**
  - `employee-validation-request`: Solicitud de validación
  - `access-checkin-request`: Solicitud de registro de entrada
  - `saga-completed`: Saga completada exitosamente
  - `saga-failed`: Saga fallida
  - `alerts`: Alertas de negocio
  
- **Consume:**
  - `employee-validation-response`: Respuesta de validación
  - `access-checkin-response`: Respuesta de registro

### 2. Check-Out Saga

**Flujo:**
1. **VALIDATE_EMPLOYEE**: Valida que el empleado existe y está activo
2. **REGISTER_ACCESS**: Actualiza el registro de acceso con hora de salida

**Compensaciones:**
- Si falla validación: Termina saga con error
- Si falla registro: Termina saga con error

**Topics Kafka:**
- **Produce:**
  - `employee-validation-request`
  - `access-checkout-request`
  - `saga-completed`
  - `saga-failed`
  
- **Consume:**
  - `employee-validation-response`
  - `access-checkout-response`

## Modelo de Dominio

### Entidades

#### Saga
```java
- id: String (UUID)
- type: SagaType (CHECK_IN, CHECK_OUT)
- status: SagaStatus
- employeeId: String
- employeeName: String
- accessId: String
- errorMessage: String
- createdAt: LocalDateTime
- completedAt: LocalDateTime
- steps: List<SagaStep>
- logs: List<SagaLog>
```

#### SagaStep
```java
- stepNumber: Integer
- stepName: String
- status: StepStatus
- request: String
- response: String
- errorMessage: String
- startedAt: LocalDateTime
- completedAt: LocalDateTime
- compensated: Boolean
```

#### SagaLog
```java
- level: LogLevel (DEBUG, INFO, WARN, ERROR)
- message: String
- details: String
- timestamp: LocalDateTime
```

### Estados de Saga

```
STARTED → PENDING_EMPLOYEE_VALIDATION → EMPLOYEE_VALIDATED → 
PENDING_ACCESS_REGISTRATION → ACCESS_REGISTERED → COMPLETED

                    ↓ (en caso de error)
                  FAILED
                    ↓ (compensación)
              COMPENSATING → COMPENSATED
```

## API REST

### Endpoints

#### Iniciar Check-In
```http
POST /api/saga/check-in
Content-Type: application/json

{
  "employeeId": "123456"
}
```

**Response:**
```json
{
  "sagaId": "uuid",
  "type": "CHECK_IN",
  "status": "STARTED",
  "employeeId": "123456",
  "createdAt": "2025-11-16T10:30:00"
}
```

#### Iniciar Check-Out
```http
POST /api/saga/check-out
Content-Type: application/json

{
  "employeeId": "123456"
}
```

#### Consultar Estado de Saga
```http
GET /api/saga/{sagaId}
```

**Response:**
```json
{
  "sagaId": "uuid",
  "type": "CHECK_IN",
  "status": "COMPLETED",
  "employeeId": "123456",
  "employeeName": "Juan Pérez",
  "accessId": "access-uuid",
  "createdAt": "2025-11-16T10:30:00",
  "completedAt": "2025-11-16T10:30:05"
}
```

#### Consultar Sagas por Empleado
```http
GET /api/saga/employee/{employeeId}
```

#### Listar Todas las Sagas
```http
GET /api/saga/all
```

#### Compensar Saga
```http
POST /api/saga/{sagaId}/compensate
```

#### Health Check
```http
GET /api/saga/health
```

## Configuración

### application.properties
```properties
# PostgreSQL
spring.datasource.url=jdbc:postgresql://localhost:5432/saga_db
spring.datasource.username=postgres
spring.datasource.password=postgres

# Kafka
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=saga-orchestrator-group

# Saga Configuration
saga.timeout.seconds=30
saga.retry.max-attempts=3
saga.retry.delay-milliseconds=1000
```

### Variables de Entorno (Docker)
```yaml
SPRING_PROFILES_ACTIVE: docker
SPRING_DATASOURCE_URL: jdbc:postgresql://postgres-saga:5432/saga_db
SPRING_DATASOURCE_USERNAME: postgres
SPRING_DATASOURCE_PASSWORD: postgres
KAFKA_BOOTSTRAP_SERVERS: kafka:9092
```

## Ejecución

### Local
```bash
mvn clean package
java -jar target/saga-orchestrator-1.0.0.jar
```

### Docker
```bash
docker-compose up -d saga-orchestrator
```

## Monitoreo

### Métricas Prometheus
```
http://localhost:8085/actuator/prometheus
```

### Health Check
```
http://localhost:8085/actuator/health
```

### Métricas Disponibles
- Total de sagas iniciadas
- Sagas completadas/fallidas
- Tiempo promedio de saga
- Timeouts
- Compensaciones ejecutadas

## Timeout y Retry

### Timeout
- **Duración:** 30 segundos (configurable)
- **Verificación:** Cada 5 segundos
- **Acción:** Marca saga como FAILED y publica evento

### Retry
- **Intentos máximos:** 3 (configurable)
- **Delay entre intentos:** 1 segundo (configurable)
- **Estrategia:** Exponential backoff

## Logging

### Niveles de Log

**Saga:**
- DEBUG: Detalles de cada paso
- INFO: Inicio/fin de saga, transiciones de estado
- WARN: Compensaciones, alertas
- ERROR: Fallos, timeouts

**Kafka:**
- INFO: Mensajes enviados/recibidos
- ERROR: Errores de serialización/deserialización

### Formato
```
2025-11-16 10:30:00 - [INFO] Starting CHECK_IN saga for employee: 123456
2025-11-16 10:30:01 - [DEBUG] Executing Step 1: Validate Employee for saga uuid
2025-11-16 10:30:02 - [INFO] Employee validated successfully: Juan Pérez
2025-11-16 10:30:03 - [DEBUG] Executing Step 3: Register Access for saga uuid
2025-11-16 10:30:05 - [INFO] Access registered successfully: access-uuid
```

## Testing

### Pruebas de Integración
```bash
mvn test
```

### Pruebas Manuales con Kafka

**Publicar respuesta de validación:**
```bash
echo '{"sagaId":"uuid","isValid":true,"employeeName":"Juan Pérez"}' | \
  kafka-console-producer --broker-list localhost:9092 --topic employee-validation-response
```

**Consumir eventos de saga:**
```bash
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic saga-completed --from-beginning
```

## Diagrama de Flujo

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │ POST /check-in
       ▼
┌─────────────────────────┐
│  Saga Orchestrator      │
│  ┌─────────────────┐    │
│  │ Create Saga     │    │
│  │ STARTED         │    │
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │ Step 1:         │────┼────► employee-validation-request
│  │ Validate        │    │
│  │ Employee        │◄───┼──── employee-validation-response
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │ Step 2:         │────┼────► access-checkin-request
│  │ Register        │    │
│  │ Access          │◄───┼──── access-checkin-response
│  └────────┬────────┘    │
│           │             │
│           ▼             │
│  ┌─────────────────┐    │
│  │ COMPLETED       │────┼────► saga-completed
│  └─────────────────┘    │
└─────────────────────────┘
```

## Ventajas del Patrón Saga

1. **Consistencia eventual**: Garantiza consistencia en transacciones distribuidas
2. **Desacoplamiento**: Servicios independientes comunicados por eventos
3. **Visibilidad**: Estado completo de transacciones distribuidas
4. **Recuperación**: Compensaciones automáticas ante fallos
5. **Auditabilidad**: Logs detallados de cada paso

## Autor

Sistema de Control de Acceso - Universidad Pedagógica y Tecnológica de Colombia
