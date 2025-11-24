# 🧪 Guía de Pruebas - Sistema Control de Acceso con SAGA

## 📋 Prerequisitos

✅ Docker Desktop corriendo  
✅ Servicios levantados con `docker-compose up -d`  
✅ Postman instalado  
✅ Colección importada: `Postman-Collection-SAGA-Tests.json`

## 🚀 Verificación Inicial

### 1. Verificar que todos los contenedores estén corriendo

```powershell
docker-compose ps
```

**Esperado**: 12 contenedores en estado `Up`
- ✅ api-gateway
- ✅ login-service
- ✅ employee-service
- ✅ access-control-service
- ✅ alert-service
- ✅ saga-orchestrator
- ✅ postgres (LoginDB)
- ✅ postgres-employee (EmployeeDB puede ser MongoDB)
- ✅ postgres-saga
- ✅ kafka
- ✅ zookeeper
- ✅ prometheus

### 2. Verificar logs de servicios

```powershell
# Ver logs del API Gateway
docker-compose logs api-gateway

# Ver logs del SAGA Orchestrator
docker-compose logs saga-orchestrator

# Ver logs de Kafka
docker-compose logs kafka
```

**Esperado**: Sin errores críticos de conexión

### 3. Health Checks

```powershell
# API Gateway
curl http://localhost:8080/actuator/health

# Login Service
curl http://localhost:8081/actuator/health

# SAGA Orchestrator
curl http://localhost:8085/api/saga/health
```

**Esperado**: Respuesta `{"status":"UP"}`

---

## 🎯 Flujo Completo de Pruebas en Postman

### **Paso 1: Autenticación**

#### 1.1 Crear Usuario Admin
- **Request**: `POST /login/createuser`
- **Body**:
  ```json
  {
    "userID": "admin",
    "password": "admin123"
  }
  ```
- **Validación**: 
  - ✅ Status: `201 Created`
  - ✅ Usuario creado en base de datos `LoginDB`

#### 1.2 Obtener Token JWT
- **Request**: `POST /login/authuser`
- **Body**:
  ```json
  {
    "userID": "admin",
    "password": "admin123"
  }
  ```
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Respuesta contiene `token`
  - ✅ Token se guarda automáticamente en variable `{{token}}`

**🔍 Verificación en BD:**
```sql
-- Conectar a LoginDB (Puerto 5432)
SELECT * FROM login WHERE userid = 'admin';
```

---

### **Paso 2: Gestión de Empleados**

#### 2.1 Crear Empleado
- **Request**: `POST /employee/createemployee`
- **Headers**: `Authorization: Bearer {{token}}`
- **Body**:
  ```json
  {
    "document": "EMP12345",
    "firstname": "Juan",
    "lastname": "Pérez",
    "email": "juan.perez@empresa.com",
    "phone": "3001234567",
    "status": true
  }
  ```
- **Validación**:
  - ✅ Status: `201 Created`
  - ✅ Documento se guarda en variable `{{employee_document}}`
  - ✅ Empleado activo (`status: true`)

**🔍 Verificación en BD (MongoDB):**
```javascript
// Conectar a EmployeeDB (Puerto 27017)
use EmployeeDB
db.Employee.find({ document: "EMP12345" })
```

#### 2.2 Listar Empleados
- **Request**: `GET /employee/findallemployees`
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Array con al menos 1 empleado
  - ✅ Empleado creado aparece en listado

---

### **Paso 3: SAGA Check-In (Transacción Distribuida)**

#### 3.1 Iniciar SAGA de Entrada
- **Request**: `POST /saga/check-in`
- **Body**:
  ```json
  {
    "employeeDocument": "EMP12345"
  }
  ```
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Respuesta contiene `sagaId`
  - ✅ Estado inicial: `STARTED`

**🔍 Flujo Interno de SAGA:**

1. **SAGA Orchestrator** publica evento a Kafka:
   - Topic: `employee-validation-request`
   - Payload: `{ sagaId, employeeDocument }`

2. **Employee Service** consume evento:
   - Valida que empleado existe
   - Valida que empleado está activo
   - Publica respuesta a: `employee-validation-response`

3. **SAGA Orchestrator** recibe validación:
   - Cambia estado a: `EMPLOYEE_VALIDATED`
   - Publica evento a: `access-checkin-request`

4. **Access Control Service** consume evento:
   - Verifica que NO tenga entrada activa
   - Crea registro de check-in
   - Publica respuesta a: `access-checkin-response`

5. **SAGA Orchestrator** recibe confirmación:
   - Cambia estado a: `COMPLETED`
   - Publica evento a: `saga-completed`

**🔍 Verificación en BD PostgreSQL (AccessControlDB):**
```sql
-- Verificar registro de entrada
SELECT * FROM access 
WHERE employeeid = 'EMP12345' 
AND exitdatetime IS NULL
ORDER BY accessdatetime DESC 
LIMIT 1;
```

**🔍 Verificación en BD PostgreSQL (SAGA DB):**
```sql
-- Verificar estado de SAGA
SELECT saga_id, employee_document, status, current_step 
FROM saga_state 
WHERE employee_document = 'EMP12345'
ORDER BY started_at DESC 
LIMIT 1;
```

#### 3.2 Consultar Estado de SAGA
- **Request**: `GET /saga/{{saga_id}}`
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Estado: `COMPLETED`
  - ✅ Paso actual: `ACCESS_REGISTERED`

#### 3.3 Intentar Check-In Duplicado (Compensación SAGA)
- **Request**: `POST /saga/check-in` (mismo empleado)
- **Validación**:
  - ✅ SAGA detecta entrada activa
  - ✅ Estado: `FAILED`
  - ✅ Se publica alerta a topic `alerts`
  - ✅ NO se crea segundo registro de entrada

**🔍 Verificación de Alerta:**
```sql
-- Verificar alerta generada
SELECT * FROM alert 
WHERE code = 'EMPLOYEE_ALREADY_ENTERED'
ORDER BY timestamp DESC 
LIMIT 1;
```

---

### **Paso 4: SAGA Check-Out**

#### 4.1 Iniciar SAGA de Salida
- **Request**: `POST /saga/check-out`
- **Body**:
  ```json
  {
    "employeeDocument": "EMP12345"
  }
  ```
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Estado: `COMPLETED`
  - ✅ Registro de entrada actualizado con `exitdatetime`

**🔍 Verificación en BD:**
```sql
SELECT employeeid, accessdatetime, exitdatetime,
       EXTRACT(EPOCH FROM (exitdatetime - accessdatetime))/3600 as horas_trabajadas
FROM access 
WHERE employeeid = 'EMP12345' 
ORDER BY accessdatetime DESC 
LIMIT 1;
```

#### 4.2 Intentar Check-Out sin Check-In
- **Request**: `POST /saga/check-out` (sin entrada activa)
- **Validación**:
  - ✅ Estado: `FAILED`
  - ✅ Error: No hay entrada activa
  - ✅ Se publica alerta

---

### **Paso 5: Reportes y Consultas**

#### 5.1 Listar Todas las SAGAs
- **Request**: `GET /saga/all`
- **Validación**:
  - ✅ Status: `200 OK`
  - ✅ Array con todas las SAGAs ejecutadas
  - ✅ Estados: `COMPLETED`, `FAILED`

#### 5.2 Consultar SAGAs por Empleado
- **Request**: `GET /saga/employee/EMP12345`
- **Validación**:
  - ✅ Solo SAGAs del empleado especificado
  - ✅ Orden cronológico

#### 5.3 Reporte de Accesos por Fecha
- **Request**: `GET /access/allemployeesbydate?date=2025-11-23`
- **Validación**:
  - ✅ Lista de accesos del día
  - ✅ Incluye horas de entrada/salida

---

## 🔍 Verificación de Kafka

### Ver mensajes en topics:

```powershell
# Conectar al contenedor de Kafka
docker exec -it kafka bash

# Ver mensajes del topic de validación de empleados
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic employee-validation-request \
  --from-beginning

# Ver respuestas de validación
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic employee-validation-response \
  --from-beginning

# Ver eventos de check-in
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic access-checkin-request \
  --from-beginning

# Ver SAGAs completadas
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic saga-completed \
  --from-beginning

# Ver alertas
kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic alerts \
  --from-beginning
```

---

## 📊 Verificación de Bases de Datos

### PostgreSQL - LoginDB

```powershell
# Conectar
docker exec -it postgres psql -U postgres -d LoginDB

# Consultas
SELECT * FROM login;
```

### MongoDB - EmployeeDB

```powershell
# Conectar
docker exec -it mongodb mongosh

# Consultas
use EmployeeDB
db.Employee.find().pretty()
db.Employee.countDocuments({ status: true })
```

### PostgreSQL - AccessControlDB

```powershell
# Conectar
docker exec -it postgres psql -U postgres -d AccessControlDB

# Consultas
SELECT * FROM access ORDER BY accessdatetime DESC LIMIT 10;
SELECT * FROM alert ORDER BY timestamp DESC LIMIT 10;

# Empleados con entrada activa
SELECT employeeid, accessdatetime 
FROM access 
WHERE exitdatetime IS NULL;
```

### PostgreSQL - SAGA DB

```powershell
# Conectar
docker exec -it postgres-saga psql -U postgres -d SagaDB

# Consultas
SELECT * FROM saga_state ORDER BY started_at DESC LIMIT 10;

# SAGAs por estado
SELECT status, COUNT(*) 
FROM saga_state 
GROUP BY status;

# SAGAs fallidas
SELECT * FROM saga_state WHERE status = 'FAILED';
```

---

## 🎭 Escenarios de Prueba Adicionales

### Escenario 1: Empleado Inactivo
```json
// 1. Crear empleado inactivo
POST /employee/createemployee
{
  "document": "EMP99999",
  "firstname": "Inactivo",
  "status": false
}

// 2. Intentar check-in
POST /saga/check-in
{
  "employeeDocument": "EMP99999"
}

// Resultado esperado: SAGA FAILED - Empleado inactivo
```

### Escenario 2: Empleado No Existe
```json
POST /saga/check-in
{
  "employeeDocument": "NOEXISTE"
}

// Resultado: SAGA FAILED - Empleado no encontrado
```

### Escenario 3: Múltiples Empleados Concurrentes
```
1. Crear 5 empleados
2. Ejecutar check-in de todos simultáneamente
3. Verificar que cada SAGA se procesa correctamente
4. Confirmar orden de eventos en Kafka
```

### Escenario 4: Compensación Manual
```json
// Si una SAGA queda en estado inconsistente
POST /saga/{sagaId}/compensate

// Verificar que se ejecutan acciones de compensación
```

---

## ✅ Checklist de Validación

### Funcionalidad
- [ ] Autenticación genera token JWT válido
- [ ] CRUD de empleados funciona correctamente
- [ ] SAGA Check-In completa exitosamente
- [ ] SAGA Check-Out completa exitosamente
- [ ] Validaciones de negocio funcionan (entrada duplicada, salida sin entrada)
- [ ] Compensaciones se ejecutan correctamente
- [ ] Alertas se generan en casos de error

### Kafka
- [ ] Topics creados automáticamente
- [ ] Mensajes se publican correctamente
- [ ] Consumidores procesan mensajes
- [ ] Sin mensajes perdidos en topics

### Bases de Datos
- [ ] LoginDB almacena usuarios
- [ ] EmployeeDB almacena empleados
- [ ] AccessControlDB registra entradas/salidas
- [ ] SagaDB persiste estados de SAGA
- [ ] AlertDB registra alertas

### API Gateway
- [ ] Rutas funcionan correctamente
- [ ] JWT se valida en endpoints protegidos
- [ ] Circuit Breaker responde con fallback cuando servicio está caído
- [ ] CORS permite requests del frontend
- [ ] Logging registra todas las peticiones

### Performance
- [ ] Check-In completa en < 5 segundos
- [ ] Check-Out completa en < 3 segundos
- [ ] Sin timeouts en SAGA
- [ ] Kafka responde rápidamente

---

## 🐛 Troubleshooting

### Servicio no responde
```powershell
# Ver logs
docker-compose logs <servicio>

# Reiniciar servicio
docker-compose restart <servicio>
```

### Kafka no recibe mensajes
```powershell
# Verificar que Kafka esté corriendo
docker-compose logs kafka

# Reiniciar Kafka y Zookeeper
docker-compose restart zookeeper kafka
```

### SAGA se queda en PENDING
```powershell
# Verificar que employee-service y access-control-service estén corriendo
docker-compose ps

# Ver logs del orquestrador
docker-compose logs saga-orchestrator

# Verificar topics de Kafka
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Error de conexión a BD
```powershell
# Verificar que PostgreSQL esté corriendo
docker-compose ps postgres

# Ver logs de BD
docker-compose logs postgres

# Reiniciar BD
docker-compose restart postgres
```

---

## 📈 Monitoreo con Prometheus/Grafana

### Prometheus
- URL: http://localhost:9090
- Métricas SAGA:
  - `saga_completed_total`
  - `saga_failed_total`
  - `saga_duration_seconds`

### Grafana
- URL: http://localhost:3000
- Usuario: `admin`
- Password: `admin123`

---

## 🎯 Métricas de Éxito

Una prueba exitosa debe cumplir:

✅ **100% de SAGAs de Check-In exitosas** (empleado válido y activo)  
✅ **100% de SAGAs de Check-Out exitosas** (con check-in previo)  
✅ **0% de SAGAs en estado PENDING** (después de 10 segundos)  
✅ **Alertas generadas** para todos los casos de error  
✅ **Consistencia en BD** (registros en Access coinciden con SAGAs COMPLETED)  
✅ **Sin errores en logs** de servicios críticos  

---

**¡Listo para probar! 🚀**
