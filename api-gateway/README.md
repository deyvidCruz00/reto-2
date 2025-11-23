# API Gateway - Sistema de Control de Acceso

Gateway centralizado implementado con Spring Cloud Gateway que maneja:
- ✅ Enrutamiento a todos los microservicios
- ✅ Autenticación JWT centralizada
- ✅ Circuit Breaker con Resilience4j
- ✅ Logging global de requests
- ✅ CORS configuration
- ✅ Métricas Prometheus

## 🚀 Tecnologías

- **Spring Boot 3.2.0**
- **Spring Cloud Gateway 2023.0.0**
- **Resilience4j** - Circuit Breaker
- **JJWT 0.12.3** - JWT Validation
- **Micrometer** - Métricas

## 📡 Rutas Configuradas

| Ruta | Servicio | Autenticación | Circuit Breaker |
|------|----------|---------------|-----------------|
| `/login/**` | Login Service (8081) | ❌ No | ❌ No |
| `/employee/**` | Employee Service (8082) | ✅ JWT | ✅ Sí |
| `/access/**` | Access Control Service (8083) | ✅ JWT | ✅ Sí |
| `/alert/**` | Alert Service (8084) | ✅ JWT | ✅ Sí |
| `/saga/**` | SAGA Orchestrator (8085) | ✅ JWT | ✅ Sí |

## 🔐 Autenticación

### Obtener Token JWT

```bash
# Login
curl -X POST http://localhost:8080/login/authuser \
  -H "Content-Type: application/json" \
  -d '{"userId":"admin","password":"admin123"}'

# Respuesta
{
  "token": "eyJhbGciOiJIUzUxMiJ9...",
  "success": true
}
```

### Usar Token en Requests

```bash
curl -X GET http://localhost:8080/employee/findallemployees \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🛡️ Circuit Breaker

Configuración Resilience4j:
- **Sliding Window Size**: 10 requests
- **Failure Rate Threshold**: 50%
- **Wait Duration (Open State)**: 10 segundos
- **Timeout**: 5 segundos (10s para SAGA)

### Endpoints de Fallback

Cuando un servicio no está disponible:

```bash
GET /fallback/employee  # Employee Service down
GET /fallback/access    # Access Control Service down
GET /fallback/alert     # Alert Service down
GET /fallback/saga      # SAGA Orchestrator down
```

Respuesta:
```json
{
  "error": true,
  "message": "Employee Service is temporarily unavailable",
  "status": 503
}
```

## 📊 Monitoreo

### Health Check

```bash
curl http://localhost:8080/health
```

### Métricas Prometheus

```bash
curl http://localhost:8080/actuator/prometheus
```

### Gateway Routes

```bash
curl http://localhost:8080/actuator/gateway/routes
```

## 🔧 Configuración

### Variables de Entorno

```yaml
# JWT
JWT_SECRET: mySecretKeyForJWTTokenGenerationAndValidation12345678901234567890
JWT_EXPIRATION: 86400000  # 24 horas

# Spring Profile
SPRING_PROFILES_ACTIVE: docker
```

### application.yml

Configuración de rutas, circuit breaker, timeouts y CORS.

## 🏃 Ejecución

### Local

```bash
mvn clean package
java -jar target/api-gateway.jar
```

### Docker

```bash
docker-compose up -d api-gateway
```

## 📝 Ejemplos de Uso

### 1. Login (Público)

```bash
POST http://localhost:8080/login/authuser
Content-Type: application/json

{
  "userId": "admin",
  "password": "admin123"
}
```

### 2. Crear Empleado (Protegido)

```bash
POST http://localhost:8080/employee/createemployee
Authorization: Bearer {token}
Content-Type: application/json

{
  "document": "123456789",
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

### 3. Check-In via SAGA (Protegido)

```bash
POST http://localhost:8080/saga/check-in
Authorization: Bearer {token}
Content-Type: application/json

{
  "employeeId": "123456789"
}
```

### 4. Consultar Alertas (Protegido)

```bash
GET http://localhost:8080/alert/all
Authorization: Bearer {token}
```

## 🔍 Logging

Todos los requests son logueados:

```
2025-11-23 10:30:00 - Incoming Request: POST /employee/createemployee from /127.0.0.1:54321
2025-11-23 10:30:00 - JWT validated successfully for user: admin
2025-11-23 10:30:01 - Outgoing Response: POST /employee/createemployee - Status: 201 - Duration: 245ms
```

## 🚨 Manejo de Errores

| Código | Descripción |
|--------|-------------|
| 401 | Missing o invalid Authorization header |
| 403 | Token JWT inválido o expirado |
| 503 | Servicio no disponible (Circuit Breaker abierto) |
| 504 | Timeout (>5s para servicios, >10s para SAGA) |

## 🎯 Features Implementadas

- ✅ Enrutamiento dinámico a 5 microservicios
- ✅ Validación JWT centralizada
- ✅ Circuit Breaker por servicio
- ✅ Logging global de requests/responses
- ✅ CORS habilitado para frontend
- ✅ Métricas Prometheus
- ✅ Health checks
- ✅ Fallback endpoints
- ✅ Timeout configuration
- ✅ Header forwarding (X-User-Id)

## 📖 Autor

Sistema de Control de Acceso - Universidad Pedagógica y Tecnológica de Colombia
