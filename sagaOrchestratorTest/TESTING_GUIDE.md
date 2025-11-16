# 🧪 Guía de Pruebas del Saga Orchestrator

## 📋 Pre-requisitos

- ✅ Maven instalado
- ✅ Docker Desktop corriendo
- ✅ Postman instalado (o usa curl)

## 🚀 Paso 1: Compilar y Levantar Servicios

### 1.1 Compilar el Proyecto

```bash
cd "c:\Users\luise\Documents\DOCS UNIVERSIDAD\2025-2\software 2\proyecto final\reto-2\saga-orchestrator"
mvn clean package -DskipTests
```

**Resultado esperado**: `BUILD SUCCESS` y archivo `target/saga-orchestrator-1.0.0.jar` creado

### 1.2 Levantar Infraestructura

```bash
cd "c:\Users\luise\Documents\DOCS UNIVERSIDAD\2025-2\software 2\proyecto final\reto-2"

# Levantar bases de datos y Kafka
docker-compose up -d postgres-saga zookeeper kafka

# Esperar 30 segundos para que inicien
timeout /t 30

# Verificar que están corriendo
docker-compose ps
```

**Resultado esperado**: 
- postgres-saga: `Up (healthy)`
- zookeeper: `Up (healthy)`
- kafka: `Up (healthy)`

### 1.3 Levantar Saga Orchestrator

```bash
# Construir y levantar
docker-compose build saga-orchestrator
docker-compose up -d saga-orchestrator

# Ver logs
docker-compose logs -f saga-orchestrator
```

**Resultado esperado**: 
```
Started SagaOrchestratorApplication in X.XXX seconds
```

Presiona `Ctrl+C` para salir de los logs.

## ✅ Paso 2: Verificar que Funciona

### 2.1 Health Check Básico

```bash
curl http://localhost:8085/api/saga/health
```

**Respuesta esperada**: `Saga Orchestrator is running`

### 2.2 Health Check de Actuator

```bash
curl http://localhost:8085/actuator/health
```

**Respuesta esperada**:
```json
{
  "status": "UP"
}
```

## 📬 Paso 3: Importar Colección de Postman

1. Abre Postman
2. Click en **Import** (esquina superior izquierda)
3. Click en **files**
4. Selecciona el archivo: `saga-orchestrator/Saga-Orchestrator.postman_collection.json`
5. Click en **Import**

Verás una colección llamada **"Saga Orchestrator API"** con 9 requests.

## 🧪 Paso 4: Pruebas con Postman

### Prueba 1: Health Check ✅

**Request**: `Health Check`

**Método**: GET  
**URL**: `http://localhost:8085/api/saga/health`

**Resultado esperado**:
```
Saga Orchestrator is running
```

---

### Prueba 2: Iniciar Check-In Saga ✅

**Request**: `Start Check-In Saga`

**Método**: POST  
**URL**: `http://localhost:8085/api/saga/check-in`  
**Body**:
```json
{
    "employeeId": "123456"
}
```

**Resultado esperado**:
```json
{
    "sagaId": "550e8400-e29b-41d4-a716-446655440000",
    "type": "CHECK_IN",
    "status": "PENDING_EMPLOYEE_VALIDATION",
    "employeeId": "123456",
    "employeeName": null,
    "accessId": null,
    "errorMessage": null,
    "createdAt": "2025-11-16T10:30:00",
    "completedAt": null
}
```

**📝 IMPORTANTE**: Copia el `sagaId` para las siguientes pruebas.

---

### Prueba 3: Consultar Estado de Saga ✅

**Request**: `Get Saga by ID`

**Método**: GET  
**URL**: `http://localhost:8085/api/saga/{sagaId}`

**Pasos**:
1. En la URL, reemplaza `:sagaId` con el ID que copiaste
2. Ejemplo: `http://localhost:8085/api/saga/550e8400-e29b-41d4-a716-446655440000`
3. Click en **Send**

**Resultado esperado**:
```json
{
    "sagaId": "550e8400-e29b-41d4-a716-446655440000",
    "type": "CHECK_IN",
    "status": "PENDING_EMPLOYEE_VALIDATION",
    "employeeId": "123456",
    "employeeName": null,
    "accessId": null,
    "errorMessage": null,
    "createdAt": "2025-11-16T10:30:00",
    "completedAt": null
}
```

**⚠️ NOTA**: El estado será `PENDING_EMPLOYEE_VALIDATION` porque aún no hay servicios de Employee y Access Control respondiendo. Esto es NORMAL.

---

### Prueba 4: Listar Todas las Sagas ✅

**Request**: `Get All Sagas`

**Método**: GET  
**URL**: `http://localhost:8085/api/saga/all`

**Resultado esperado**:
```json
[
    {
        "sagaId": "550e8400-e29b-41d4-a716-446655440000",
        "type": "CHECK_IN",
        "status": "PENDING_EMPLOYEE_VALIDATION",
        "employeeId": "123456",
        ...
    }
]
```

---

### Prueba 5: Consultar Sagas por Empleado ✅

**Request**: `Get Sagas by Employee`

**Método**: GET  
**URL**: `http://localhost:8085/api/saga/employee/123456`

**Resultado esperado**:
```json
[
    {
        "sagaId": "550e8400-e29b-41d4-a716-446655440000",
        "type": "CHECK_IN",
        "status": "PENDING_EMPLOYEE_VALIDATION",
        "employeeId": "123456",
        ...
    }
]
```

---

### Prueba 6: Iniciar Check-Out Saga ✅

**Request**: `Start Check-Out Saga`

**Método**: POST  
**URL**: `http://localhost:8085/api/saga/check-out`  
**Body**:
```json
{
    "employeeId": "789012"
}
```

**Resultado esperado**:
```json
{
    "sagaId": "nuevo-saga-id",
    "type": "CHECK_OUT",
    "status": "PENDING_EMPLOYEE_VALIDATION",
    "employeeId": "789012",
    ...
}
```

---

### Prueba 7: Métricas Prometheus ✅

**Request**: `Prometheus Metrics`

**Método**: GET  
**URL**: `http://localhost:8085/actuator/prometheus`

**Resultado esperado**: Texto con métricas como:
```
# HELP jvm_memory_used_bytes The amount of used memory
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap",id="PS Eden Space",} 1.23456789E8
...
```

---

## 🔍 Paso 5: Verificar en la Base de Datos

### 5.1 Conectar a PostgreSQL

```bash
docker exec -it postgres-saga-db psql -U postgres -d saga_db
```

### 5.2 Ver Sagas Creadas

```sql
-- Ver todas las sagas
SELECT id, type, status, employee_id, created_at 
FROM sagas 
ORDER BY created_at DESC;

-- Ver pasos de una saga específica
SELECT step_number, step_name, status, started_at, completed_at
FROM saga_steps 
WHERE saga_id = 'TU_SAGA_ID'
ORDER BY step_number;

-- Ver logs de una saga
SELECT level, message, details, timestamp
FROM saga_logs
WHERE saga_id = 'TU_SAGA_ID'
ORDER BY timestamp;
```

### 5.3 Salir de PostgreSQL

```sql
\q
```

---

## 📊 Paso 6: Verificar Kafka (Opcional)

### 6.1 Ver Topics Creados

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
```

**Deberías ver**:
- employee-validation-request
- employee-validation-response
- access-checkin-request
- access-checkin-response
- access-checkout-request
- access-checkout-response
- saga-completed
- saga-failed
- alerts

### 6.2 Consumir Mensajes de Kafka

```bash
# Ver mensajes de validación de empleado
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic employee-validation-request \
  --from-beginning

# Presiona Ctrl+C para salir
```

**Deberías ver** un mensaje JSON como:
```json
{"sagaId":"550e8400...","employeeId":"123456","action":"CHECK_IN"}
```

---

## 🎯 Paso 7: Simular Respuestas de Kafka (Prueba Completa)

Como los servicios de Employee y Access Control aún no están integrados, podemos simular sus respuestas manualmente.

### 7.1 Simular Respuesta de Validación de Empleado

```bash
# Reemplaza SAGA_ID con el ID de tu saga
echo "{\"sagaId\":\"SAGA_ID\",\"isValid\":true,\"employeeName\":\"Juan Pérez\",\"errorMessage\":null}" | docker exec -i kafka kafka-console-producer --broker-list localhost:9092 --topic employee-validation-response
```

### 7.2 Verificar que la Saga Avanzó

En Postman, ejecuta nuevamente `Get Saga by ID` con tu sagaId.

**Deberías ver**:
```json
{
    "status": "PENDING_ACCESS_REGISTRATION",
    "employeeName": "Juan Pérez",
    ...
}
```

### 7.3 Simular Respuesta de Registro de Acceso

```bash
# Reemplaza SAGA_ID con el ID de tu saga
echo "{\"sagaId\":\"SAGA_ID\",\"success\":true,\"accessId\":\"access-123\",\"errorMessage\":null}" | docker exec -i kafka kafka-console-producer --broker-list localhost:9092 --topic access-checkin-response
```

### 7.4 Verificar que la Saga Completó

En Postman, ejecuta nuevamente `Get Saga by ID`.

**Deberías ver**:
```json
{
    "status": "COMPLETED",
    "employeeName": "Juan Pérez",
    "accessId": "access-123",
    "completedAt": "2025-11-16T10:31:00"
}
```

---

## ✅ Checklist de Pruebas

- [ ] Servicio inicia correctamente (logs sin errores)
- [ ] Health check responde OK
- [ ] Puedo crear saga de check-in
- [ ] Puedo consultar saga por ID
- [ ] Puedo listar todas las sagas
- [ ] Puedo consultar sagas por empleado
- [ ] Puedo crear saga de check-out
- [ ] Sagas se guardan en base de datos
- [ ] Kafka produce mensajes de validación
- [ ] Métricas Prometheus disponibles

---

## 🐛 Troubleshooting

### Problema 1: "Connection refused" en localhost:8085

**Solución**:
```bash
# Verificar que el servicio está corriendo
docker-compose ps saga-orchestrator

# Ver logs
docker-compose logs saga-orchestrator

# Reiniciar
docker-compose restart saga-orchestrator
```

### Problema 2: Base de datos no conecta

**Solución**:
```bash
# Verificar postgres-saga
docker-compose ps postgres-saga

# Ver logs
docker-compose logs postgres-saga

# Reiniciar ambos
docker-compose restart postgres-saga
docker-compose restart saga-orchestrator
```

### Problema 3: Kafka no conecta

**Solución**:
```bash
# Verificar Kafka
docker-compose ps kafka

# Reiniciar Kafka
docker-compose restart zookeeper
docker-compose restart kafka
docker-compose restart saga-orchestrator
```

### Problema 4: "Port 8085 already in use"

**Solución**:
```bash
# Encontrar proceso usando puerto 8085
netstat -ano | findstr :8085

# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F

# Reiniciar servicio
docker-compose up -d saga-orchestrator
```

---

## 📝 Logs Útiles

### Ver todos los logs del saga-orchestrator

```bash
docker-compose logs -f saga-orchestrator
```

### Ver últimas 50 líneas

```bash
docker-compose logs --tail=50 saga-orchestrator
```

### Ver logs con timestamp

```bash
docker-compose logs -t saga-orchestrator
```

---

## 🎉 ¡Pruebas Exitosas!

Si completaste todas las pruebas, tu Saga Orchestrator está funcionando correctamente. 

### Próximos pasos:

1. **Integrar Employee Service** para responder validaciones automáticamente
2. **Integrar Access Control Service** para registrar accesos
3. **Integrar Alert Service** para procesar alertas
4. **Pruebas end-to-end** completas

Consulta `INTEGRATION_GUIDE.md` para los detalles de integración.

---


