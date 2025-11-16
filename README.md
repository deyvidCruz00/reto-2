# Sistema de Control de Acceso - Arquitectura SAGA

## 📋 Descripción del Proyecto

Sistema de información para el control de acceso peatonal a las instalaciones de una empresa, desarrollado con arquitectura de microservicios, Event-Driven Architecture (EDA), patrón SAGA para mantener consistencia distribuida y arquitectura hexagonal.

## 🏗️ Arquitectura

### Microservicios

1. **API Gateway** (Puerto 8080)
   - Punto de entrada único al sistema
   - Enrutamiento de peticiones
   - Autenticación y autorización centralizada

2. **Login Service** (Puerto 8081)
   - Gestión de usuarios del sistema
   - Autenticación con JWT
   - PostgreSQL (LoginDB)

3. **Employee Service** (Puerto 8082)
   - Gestión de empleados (CRUD)
   - MongoDB (EmployeeDB) - Base de datos NoSQL
   - Arquitectura hexagonal con DDD

4. **Access Control Service** (Puerto 8083)
   - Registro de entradas/salidas
   - Generación de reportes
   - PostgreSQL (AccessControlDB)

5. **Alert Service** (Puerto 8084)
   - Gestión de alertas del sistema
   - PostgreSQL (AccessControlDB)

6. **SAGA Orchestrator** (Puerto 8085)
   - Coordinación de transacciones distribuidas
   - Manejo de compensaciones en caso de fallo
   - Orquestación de eventos Kafka

### Tecnologías Utilizadas

- **Backend**: Spring Boot 3.2.0 con Java 17
- **Bases de Datos**: 
  - PostgreSQL 15 (Relacional)
  - MongoDB 7.0 (NoSQL)
- **Event Bus**: Apache Kafka 7.5.0
- **Monitoreo**: Prometheus + Grafana
- **Contenedorización**: Docker & Docker Compose
- **ORM**: Spring Data JPA y Spring Data MongoDB
- **Seguridad**: Spring Security + JWT
- **Documentación API**: SpringDoc OpenAPI (Swagger)

## 📦 Estructura del Proyecto

```
reto-2/
├── api-gateway/                 # Gateway de entrada
├── login-service/               # Microservicio de autenticación
├── employee-service/            # Microservicio de empleados
├── access-control-service/      # Microservicio de control de acceso
├── alert-service/               # Microservicio de alertas
├── saga-orchestrator/           # Orquestador SAGA
├── frontend/                    # Aplicación web (React/Angular/Vue)
├── monitoring/                  # Configuración Prometheus/Grafana
├── docker/                      # Scripts de inicialización BD
└── docker-compose.yml           # Configuración de contenedores
```

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Docker Desktop instalado
- Java 17 JDK
- Maven 3.8+
- Node.js 18+ (para frontend)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd reto-2
```

2. **Construir los microservicios**
```bash
# Construir todos los servicios
mvn clean package -DskipTests

# O construir individualmente cada servicio
cd login-service && mvn clean package -DskipTests && cd ..
cd employee-service && mvn clean package -DskipTests && cd ..
cd access-control-service && mvn clean package -DskipTests && cd ..
cd alert-service && mvn clean package -DskipTests && cd ..
cd saga-orchestrator && mvn clean package -DskipTests && cd ..
cd api-gateway && mvn clean package -DskipTests && cd ..
```

3. **Levantar la infraestructura con Docker Compose**
```bash
docker-compose up -d
```

4. **Verificar que todos los servicios estén corriendo**
```bash
docker-compose ps
```

### URLs de Acceso

- **API Gateway**: http://localhost:8080
- **Login Service**: http://localhost:8081
- **Employee Service**: http://localhost:8082
- **Access Control Service**: http://localhost:8083
- **Alert Service**: http://localhost:8084
- **SAGA Orchestrator**: http://localhost:8085
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Frontend**: http://localhost:4200

### Documentación API (Swagger)

- **API Gateway Swagger**: http://localhost:8080/swagger-ui.html
- **Login Service**: http://localhost:8081/swagger-ui.html
- **Employee Service**: http://localhost:8082/swagger-ui.html
- **Access Control Service**: http://localhost:8083/swagger-ui.html
- **Alert Service**: http://localhost:8084/swagger-ui.html

## 🔐 Endpoints Principales

### Login Service (`/login`)
- `POST /login/createuser` - Registrar usuario
- `POST /login/authuser` - Autenticar usuario

### Employee Service (`/employee`)
- `POST /employee/createemployee` - Crear empleado
- `PUT /employee/updateemployee` - Actualizar empleado
- `GET /employee/findallemployees` - Listar todos los empleados
- `PUT /employee/disableemployee/{document}` - Inactivar empleado

### Access Control Service (`/access`)
- `POST /access/usercheckin` - Registrar entrada
- `POST /access/usercheckout` - Registrar salida
- `GET /access/allemployeesbydate` - Reporte por fecha
- `GET /access/employeebydates` - Reporte por empleado y rango de fechas

### Alert Service (`/alert`)
- `POST /alert/usrnotregistattempt` - Alerta usuario no registrado
- `POST /alert/usrexceedattempts` - Alerta intentos excedidos

### SAGA Orchestrator (`/api/saga`)
- `POST /api/saga/check-in` - Iniciar saga de check-in
- `POST /api/saga/check-out` - Iniciar saga de check-out
- `GET /api/saga/{sagaId}` - Consultar estado de saga
- `GET /api/saga/employee/{employeeId}` - Listar sagas por empleado
- `GET /api/saga/all` - Listar todas las sagas
- `POST /api/saga/{sagaId}/compensate` - Compensar saga fallida
- `POST /alert/employeealreadyentered` - Alerta entrada duplicada
- `POST /alert/employeealreadyleft` - Alerta salida duplicada

## 🏛️ Patrón SAGA con Orquestación

El sistema implementa el patrón **SAGA Orchestration** con un orquestador centralizado para manejar transacciones distribuidas y garantizar consistencia eventual.

### Características

- **Orquestador centralizado** en puerto 8085
- **Persistencia de estado** en PostgreSQL dedicado
- **Comunicación asíncrona** vía Kafka
- **Compensación automática** en caso de fallos
- **Timeout handling** (30 segundos configurable)
- **Logging detallado** de cada paso

### Check-In SAGA

**Pasos:**
1. **VALIDATE_EMPLOYEE**: Valida empleado existe y está activo
2. **CHECK_ACTIVE_ENTRY**: Verifica no tiene entrada activa  
3. **REGISTER_ACCESS**: Registra entrada en Access Control

**Compensaciones:**
- Fallo en paso 3 → Publica alerta `EMPLOYEE_ALREADY_ENTERED`
- Fallo en validación → Termina saga con error

### Check-Out SAGA

**Pasos:**
1. **VALIDATE_EMPLOYEE**: Valida empleado existe y está activo
2. **REGISTER_ACCESS**: Actualiza registro con hora de salida

**Compensaciones:**
- Fallo en cualquier paso → Termina saga con error

### Estados de SAGA

```
STARTED → PENDING_EMPLOYEE_VALIDATION → EMPLOYEE_VALIDATED → 
PENDING_ACCESS_REGISTRATION → ACCESS_REGISTERED → COMPLETED

              ↓ (error)
            FAILED
              ↓ (compensación)
        COMPENSATING → COMPENSATED
```

### Flujo de Eventos Kafka

```
Topics Producidos por Orchestrator:
- employee-validation-request    (solicitud validación empleado)
- access-checkin-request         (solicitud registro entrada)
- access-checkout-request        (solicitud registro salida)
- saga-completed                 (saga exitosa)
- saga-failed                    (saga fallida)
- alerts                         (alertas de negocio)

Topics Consumidos por Orchestrator:
- employee-validation-response   (respuesta validación empleado)
- access-checkin-response        (respuesta registro entrada)
- access-checkout-response       (respuesta registro salida)
```


## 📊 Monitoreo

### Prometheus Metrics

Cada microservicio expone métricas en `/actuator/prometheus`:
- Número de peticiones HTTP
- Tiempo de respuesta
- Estado de salud
- Uso de CPU/Memoria
- Transacciones SAGA

### Dashboards Grafana

Dashboards preconfigurados para:
- Estado de microservicios
- Métricas de Kafka
- Performance de base de datos
- Alertas del sistema

## 🔒 Seguridad

- **Autenticación**: JWT (JSON Web Tokens)
- **Autorización**: Role-Based Access Control (RBAC)
- **Encriptación**: Contraseñas con BCrypt
- **Bloqueo**: Bloqueo temporal tras 3 intentos fallidos (10 minutos)

## 🧪 Testing

```bash
# Ejecutar tests unitarios
mvn test

# Ejecutar tests de integración
mvn verify
```

## 📝 Base de Datos

### PostgreSQL - LoginDB
- Tabla: Login (id, userID, password)

### MongoDB - EmployeeDB
- Colección: Employee (document, firstname, lastname, email, phone, status)

### PostgreSQL - AccessControlDB
- Tabla: Access (employeeID, accessdatetime, exitdatetime)
- Tabla: Alert (ID, Timestamp, Description, Code)

## 👥 Atributos de Calidad

- ✅ **Escalabilidad**: Arquitectura de microservicios
- ✅ **Resiliencia**: Patrón SAGA con compensaciones
- ✅ **Observabilidad**: Prometheus + Grafana
- ✅ **Seguridad**: JWT + Autenticación multifactor
- ✅ **Mantenibilidad**: Arquitectura hexagonal + DDD

## 📚 Documentación Adicional

Ver carpetas individuales de cada microservicio para documentación específica.

## 🤝 Contribuidores

UPTC - Ingeniería de Software II - Segundo Corte

## 📄 Licencia

Este proyecto es desarrollado con fines académicos.
