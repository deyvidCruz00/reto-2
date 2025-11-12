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
- `POST /alert/employeealreadyentered` - Alerta entrada duplicada
- `POST /alert/employeealreadyleft` - Alerta salida duplicada

## 🏛️ Patrón SAGA

El sistema implementa el patrón **SAGA Orchestration** para manejar transacciones distribuidas:

### Ejemplo: Registro de Acceso (Check-In)

1. **Inicio**: Usuario solicita registrar entrada
2. **Validación Empleado**: SAGA verifica que el empleado exista
3. **Verificación Estado**: SAGA verifica que no tenga entrada activa
4. **Registro**: Se registra la entrada en Access Control Service
5. **Evento Éxito**: Se publica evento de éxito
6. **Compensación** (si falla): Se revierten los cambios

### Flujo de Eventos Kafka

```
Topics:
- employee-validation-request
- employee-validation-response
- access-checkin-request
- access-checkin-response
- access-checkout-request
- access-checkout-response
- alert-notification
- saga-compensation
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
