# 📋 Plan de Desarrollo - Equipo de 3 Personas

## 🎯 Objetivo

Completar el **33% restante** del proyecto de Sistema de Control de Acceso, pasando del 67% actual al 100% en **3 semanas**.

---

## 📊 Estado Actual del Proyecto

### ✅ Completado (67%)
- ✅ Infraestructura completa (Docker, PostgreSQL, MongoDB, Kafka, Prometheus, Grafana)
- ✅ Login Service (Spring Boot) - 100%
- ✅ Employee Service (Flask/Python) - 100%
- ✅ Access Control Service (Flask/Python) - 100%
- ✅ Alert Service (Spring Boot) - 100%

### 🔄 Pendiente (33%)
- ⏳ SAGA Orchestrator Service (Spring Boot) - 0%
- ⏳ API Gateway (Spring Cloud Gateway) - 0%
- ⏳ Frontend (React/Angular/Vue) - 0%
- ⏳ Documentación UML (Diagramas) - 0%
- ⏳ Testing E2E - 0%

---

## 👥 Distribución del Equipo

### **Persona 1: Backend Senior (SAGA + Integraciones)**
**Enfoque**: Arquitectura distribuida, orquestación de transacciones, coordinación de microservicios

### **Persona 2: Backend/Fullstack (API Gateway + Testing)**
**Enfoque**: Gateway, seguridad, pruebas de integración, documentación técnica

### **Persona 3: Frontend Developer (UI/UX + Documentación)**
**Enfoque**: Aplicación web, experiencia de usuario, diagramas UML

---

## 📅 Plan de 3 Semanas

---

# 🗓️ SEMANA 1: BACKEND AVANZADO

## **Persona 1: SAGA Orchestrator Service**

### Objetivo
Implementar el orquestador SAGA completo para coordinar transacciones distribuidas entre Employee, Access Control y Alert services.

### Tareas (32 horas)

#### **Día 1-2: Diseño y Estructura Base (12h)**
- [x] Crear proyecto Spring Boot con dependencias (Kafka, Actuator, Prometheus)
- [x] Definir modelo de dominio para Sagas (SagaState, SagaStep, SagaCompensation)
- [x] Implementar entidades JPA para persistir estado de sagas
- [x] Configurar conexión a PostgreSQL para estado de sagas
- [x] Configurar Kafka consumer/producer
- [x] Implementar estructura hexagonal (Domain → Application → Infrastructure)

**Archivos a crear:**
```
saga-orchestrator/
├── pom.xml
├── Dockerfile
├── src/main/java/com/uptc/sagaorchestrator/
│   ├── SagaOrchestratorApplication.java
│   ├── domain/
│   │   ├── entity/
│   │   │   ├── Saga.java
│   │   │   ├── SagaStep.java
│   │   │   └── SagaLog.java
│   │   └── port/
│   │       ├── SagaRepositoryPort.java
│   │       └── SagaUseCasePort.java
│   ├── application/
│   │   ├── dto/
│   │   │   ├── CheckInRequest.java
│   │   │   ├── CheckOutRequest.java
│   │   │   └── SagaResponse.java
│   │   └── service/
│   │       ├── CheckInSagaService.java
│   │       └── CheckOutSagaService.java
│   └── infrastructure/
│       ├── repository/
│       │   └── JpaSagaRepository.java
│       ├── kafka/
│       │   ├── SagaKafkaProducer.java
│       │   ├── SagaKafkaConsumer.java
│       │   └── KafkaConfig.java
│       └── rest/
│           └── SagaController.java
```

#### **Día 3: Check-In SAGA (8h)**
- [x] Implementar `CheckInSaga` con pasos:
  1. Validar empleado existe (consume employee-validation-response)
  2. Validar empleado está activo
  3. Validar no tiene entrada activa
  4. Registrar entrada en Access Control
  5. Publicar evento success/failure
- [x] Implementar compensaciones:
  - Si falla paso 3: publicar alerta EMPLOYEE_ALREADY_ENTERED
  - Si falla paso 4: revertir validaciones
- [x] Implementar timeout handling (30 segundos)
- [x] Logging detallado de cada paso

**Topics Kafka:**
- Consume: `employee-validation-response`, `access-checkin-response`
- Produce: `employee-validation-request`, `access-checkin-request`, `saga-completed`, `saga-failed`

#### **Día 4: Check-Out SAGA (8h)**
- [x] Implementar `CheckOutSaga` con pasos:
  1. Validar empleado existe
  2. Validar empleado tiene entrada activa sin salida
  3. Registrar salida en Access Control
  4. Calcular duración
  5. Publicar evento success/failure
- [x] Implementar compensaciones:
  - Si falla paso 2: publicar alerta EMPLOYEE_ALREADY_LEFT
  - Si falla paso 3: revertir validaciones
- [x] Implementar retry mechanism (3 intentos)

#### **Día 5: Testing y Refinamiento (4h)**
- [x] Unit tests para cada saga
- [x] Integration tests con TestContainers
- [x] Pruebas de compensación (forzar fallos)
- [x] Documentación Swagger
- [x] Métricas Prometheus (sagas completadas/fallidas/compensadas)

**Entregables Persona 1:**
- ✅ SAGA Orchestrator funcionando al 100%
- ✅ Check-In y Check-Out sagas completas
- ✅ Compensaciones implementadas
- ✅ Tests con >80% cobertura
- ✅ Documentación API

---

## **Persona 2: API Gateway + Seguridad**

### Objetivo
Implementar API Gateway centralizado con Spring Cloud Gateway, autenticación JWT, rate limiting y CORS.

### Tareas (32 horas)

#### **Día 1-2: Setup y Configuración Base (12h)**
- [x] Crear proyecto Spring Cloud Gateway
- [x] Configurar dependencias (Gateway, Security, JWT, Redis, Actuator)
- [x] Implementar JWT Token Validator (reutilizar LoginService logic)
- [x] Configurar filtros de autenticación global
- [x] Implementar JwtAuthenticationFilter
- [x] Configurar CORS global

**Archivos a crear:**
```
api-gateway/
├── pom.xml
├── Dockerfile
├── src/main/
│   ├── resources/
│   │   ├── application.yml
│   │   └── application-docker.yml
│   └── java/com/uptc/apigateway/
│       ├── ApiGatewayApplication.java
│       ├── config/
│       │   ├── GatewayConfig.java
│       │   ├── SecurityConfig.java
│       │   └── CorsConfig.java
│       ├── filter/
│       │   ├── JwtAuthenticationFilter.java
│       │   └── LoggingFilter.java
│       ├── security/
│       │   ├── JwtTokenProvider.java
│       │   └── JwtTokenValidator.java
│       └── exception/
│           └── GlobalExceptionHandler.java
```

#### **Día 3: Rutas y Rate Limiting (8h)**
- [x] Configurar rutas para todos los microservicios:
  ```yaml
  routes:
    - id: login-service
      uri: lb://login-service
      predicates: [Path=/login/**]
      
    - id: employee-service
      uri: lb://employee-service
      predicates: [Path=/employee/**]
      filters: [JwtAuth]
      
    - id: access-control-service
      uri: lb://access-control-service
      predicates: [Path=/access/**]
      filters: [JwtAuth]
      
    - id: alert-service
      uri: lb://alert-service
      predicates: [Path=/alert/**]
      filters: [JwtAuth]
  ```
- [x] Implementar Rate Limiting con Redis:
  - 100 requests/min por usuario
  - 1000 requests/min global
- [x] Implementar Circuit Breaker con Resilience4j
- [x] Logging de todas las requests

#### **Día 4: Testing de Integración (8h)**
- [x] Configurar TestContainers para tests E2E
- [x] Tests de autenticación:
  - Login exitoso → recibir JWT
  - Request sin token → 401 Unauthorized
  - Token inválido → 403 Forbidden
  - Token expirado → 401 Unauthorized
- [x] Tests de rutas:
  - Cada microservicio responde correctamente
  - Circuit breaker funciona ante fallos
  - Rate limiting bloquea requests excesivas
- [x] Tests de CORS:
  - Preflight requests (OPTIONS)
  - Headers correctos

#### **Día 5: Documentación y Monitoreo (4h)**
- [x] Configurar Prometheus metrics
- [x] Crear dashboard Grafana para Gateway:
  - Requests por servicio
  - Latencia promedio
  - Rate limit violations
  - Circuit breaker status
- [x] Documentar arquitectura de Gateway
- [x] README con ejemplos de uso

**Entregables Persona 2:**
- ✅ API Gateway funcionando al 100%
- ✅ Autenticación JWT centralizada
- ✅ Rate limiting implementado
- ✅ Circuit breaker configurado
- ✅ Tests E2E pasando
- ✅ Dashboard Grafana

---

## **Persona 3: Frontend - Setup Inicial**

### Objetivo
Preparar el proyecto frontend, diseñar arquitectura de componentes y crear primeras vistas.

### Tareas (32 horas)

#### **Día 1: Setup del Proyecto (8h)**
- [x] Decisión de framework: **React** (recomendado) o Angular/Vue
- [x] Setup con Vite + React + TypeScript
- [x] Configurar estructura de carpetas:
  ```
  frontend/
  ├── src/
  │   ├── components/
  │   ├── pages/
  │   ├── services/
  │   ├── hooks/
  │   ├── context/
  │   ├── types/
  │   ├── utils/
  │   └── assets/
  ├── public/
  ├── package.json
  ├── tsconfig.json
  ├── vite.config.ts
  └── Dockerfile
  ```
- [x] Instalar dependencias:
  - React Router DOM
  - Axios
  - React Hook Form
  - TailwindCSS / Material-UI
  - React Query
  - Chart.js / Recharts
- [x] Configurar Axios con interceptors para JWT

#### **Día 2: Autenticación y Layout (8h)**
- [x] Crear AuthContext para manejo de sesión
- [x] Implementar páginas:
  - `LoginPage.tsx` - Formulario de login
  - `DashboardLayout.tsx` - Layout con sidebar y navbar
  - `ProtectedRoute.tsx` - HOC para rutas privadas
- [x] Implementar servicio de autenticación:
  ```typescript
  // src/services/authService.ts
  export const login = async (credentials)
  export const logout = ()
  export const getToken = ()
  export const isAuthenticated = ()
  ```
- [x] Configurar React Router con rutas protegidas
- [x] Diseño responsive (mobile-first)

#### **Día 3: Gestión de Empleados - CRUD (8h)**
- [x] Crear páginas:
  - `EmployeesListPage.tsx` - Tabla con todos los empleados
  - `EmployeeFormPage.tsx` - Crear/Editar empleado
- [x] Implementar componentes:
  - `EmployeeTable.tsx` - Tabla paginada con búsqueda
  - `EmployeeForm.tsx` - Formulario con validación
  - `EmployeeCard.tsx` - Card individual de empleado
- [x] Implementar servicio de empleados:
  ```typescript
  export const getEmployees = async ()
  export const createEmployee = async (data)
  export const updateEmployee = async (id, data)
  export const disableEmployee = async (id)
  ```
- [x] Validaciones de formulario con React Hook Form
- [x] Feedback visual (loading, success, error)

#### **Día 4-5: Control de Accesos + Diseño (8h)**
- [x] Crear páginas:
  - `AccessControlPage.tsx` - Check-in/Check-out rápido
  - `AccessReportsPage.tsx` - Reportes y estadísticas
- [x] Implementar componentes:
  - `QuickAccessForm.tsx` - Input rápido de documento
  - `AccessHistoryTable.tsx` - Historial de accesos
  - `AccessReportFilters.tsx` - Filtros de fecha y empleado
- [x] Implementar gráficos con Chart.js:
  - Accesos por día (gráfico de barras)
  - Duración promedio (gráfico de líneas)
  - Empleados más activos (top 10)
- [x] Implementar servicio de accesos:
  ```typescript
  export const checkIn = async (employeeId)
  export const checkOut = async (employeeId)
  export const getAccessByDate = async (date)
  export const getAccessByEmployee = async (employeeId, startDate, endDate)
  ```

**Entregables Persona 3:**
- ✅ Proyecto React configurado y funcionando
- ✅ Login funcional con JWT
- ✅ CRUD de empleados completo
- ✅ Check-in/Check-out funcional
- ✅ Reportes básicos con gráficos
- ✅ Diseño responsive

---

# 🗓️ SEMANA 2: INTEGRACIÓN Y REFINAMIENTO

## **Persona 1: Integración SAGA con Servicios Existentes**

### Tareas (32 horas)

#### **Día 1-2: Modificar Servicios Existentes (12h)**
- [x] **Employee Service**: Modificar para responder a validaciones SAGA
  - Implementar consumer Kafka para `employee-validation-request`
  - Publicar `employee-validation-response` con resultado
  - Agregar timeout handling
  
- [x] **Access Control Service**: Modificar para integrarse con SAGA
  - Cambiar `usercheckin` para usar SAGA en lugar de lógica directa
  - Cambiar `usercheckout` para usar SAGA
  - Mantener endpoints legacy para testing directo
  - Implementar consumer para `access-checkin-request`/`access-checkout-request`
  - Publicar `access-checkin-response`/`access-checkout-response`

**Archivos a modificar:**
```
employee-service/services/kafka_service.py
  - Agregar método handle_validation_request()
  - Implementar consumer dedicado

access-control-service/services/saga_service.py
  - Refactorizar para usar SAGA orchestrator
  - Implementar consumers para requests
  - Publicar responses
```

#### **Día 3: Pruebas de Integración SAGA (8h)**
- [x] Crear script de prueba completo de flujos SAGA:
  ```
  test-saga-integration.ps1:
  1. Crear empleado
  2. Check-in vía SAGA → Success
  3. Intentar check-in duplicado → Compensación + Alerta
  4. Check-out vía SAGA → Success
  5. Intentar check-out duplicado → Compensación + Alerta
  6. Verificar logs en SAGA Orchestrator
  7. Verificar alertas en Alert Service
  ```
- [x] Pruebas de compensación forzando fallos:
  - Detener Employee Service → SAGA debe compensar
  - Detener Access Control → SAGA debe compensar
  - Timeout de servicios → SAGA debe revertir
- [x] Verificar métricas en Prometheus:
  - Sagas completadas
  - Sagas fallidas
  - Compensaciones ejecutadas

#### **Día 4-5: Optimización y Resilencia (12h)**
- [x] Implementar retry con exponential backoff
- [x] Implementar dead letter queue para mensajes fallidos
- [x] Optimizar queries de base de datos en SAGA
- [x] Implementar caching con Redis para validaciones frecuentes
- [x] Documentación completa del flujo SAGA:
  - Diagramas de secuencia
  - Tabla de decisiones
  - Códigos de error
  - Tiempos de timeout

**Entregables Persona 1:**
- ✅ SAGA totalmente integrado con servicios existentes
- ✅ Compensaciones funcionando correctamente
- ✅ Scripts de prueba automatizados
- ✅ Documentación de flujos SAGA
- ✅ Optimizaciones implementadas

---

## **Persona 2: Testing E2E y Documentación Técnica**

### Tareas (32 horas)

#### **Día 1-2: Testing E2E (12h)**
- [x] Configurar framework de testing E2E:
  - **Opción 1**: Postman Collections + Newman
  - **Opción 2**: Jest + Supertest
  - **Opción 3**: Rest Assured (Java)
  
- [x] Crear colección de tests E2E:

**Suite 1: Flujo Completo de Empleado**
```
1. POST /login/createuser → Crear admin
2. POST /login/authuser → Obtener JWT
3. POST /employee/createemployee → Crear empleado
4. GET /employee/findallemployees → Verificar aparece
5. PUT /employee/updateemployee → Actualizar datos
6. PUT /employee/disableemployee → Inactivar
```

**Suite 2: Flujo Completo de Acceso**
```
1. Crear empleado activo
2. POST /access/usercheckin → Check-in exitoso
3. POST /access/usercheckin → Check-in duplicado (debe fallar)
4. GET /alert/code/EMPLOYEE_ALREADY_ENTERED → Verificar alerta
5. POST /access/usercheckout → Check-out exitoso
6. GET /access/allemployeesbydate?date=TODAY → Verificar en reporte
```

**Suite 3: Flujo SAGA**
```
1. Crear empleado
2. Iniciar Check-in SAGA → Verificar estado en orchestrator
3. Verificar evento en Kafka
4. Verificar registro en Access Control
5. Iniciar Check-out SAGA
6. Verificar duración calculada
```

**Suite 4: Seguridad y Gateway**
```
1. Request sin token → 401
2. Token inválido → 403
3. Token expirado → 401
4. Rate limiting → 429 (después de 100 requests)
5. CORS preflight → 200
```

- [x] Automatizar ejecución de tests en CI/CD
- [x] Generar reportes HTML de tests

#### **Día 3: Performance Testing (8h)**
- [x] Configurar JMeter o K6 para load testing
- [x] Tests de carga:
  - 100 usuarios concurrentes creando empleados
  - 500 check-ins simultáneos
  - 1000 consultas de reportes por minuto
- [x] Identificar y documentar bottlenecks
- [x] Sugerencias de optimización:
  - Índices de base de datos
  - Caching estratégico
  - Connection pooling

#### **Día 4-5: Documentación Técnica (12h)**
- [x] Crear **Manual de Arquitectura**:
  - Diagrama de alto nivel de microservicios
  - Explicación de cada componente
  - Flujo de datos entre servicios
  - Decisiones de diseño
  
- [x] Crear **Manual de Despliegue**:
  - Requisitos de infraestructura
  - Pasos de instalación
  - Configuración de variables de entorno
  - Troubleshooting común
  
- [x] Crear **Manual de API**:
  - Consolidar todos los endpoints
  - Ejemplos de requests/responses
  - Códigos de error
  - Rate limits y quotas
  
- [x] Crear **Manual de Operaciones**:
  - Monitoreo con Prometheus/Grafana
  - Logs y debugging
  - Backups de base de datos
  - Disaster recovery

**Entregables Persona 2:**
- ✅ Suite completa de tests E2E
- ✅ Reportes de testing automatizados
- ✅ Performance testing completado
- ✅ 4 manuales técnicos completos

---

## **Persona 3: Frontend - Funcionalidades Avanzadas**

### Tareas (32 horas)

#### **Día 1-2: Alertas y Dashboard (12h)**
- [x] Crear páginas:
  - `AlertsPage.tsx` - Vista de todas las alertas
  - `DashboardPage.tsx` - Dashboard principal con KPIs
  
- [x] Implementar componentes:
  - `AlertList.tsx` - Lista de alertas con filtros
  - `AlertFilters.tsx` - Filtros por código, severidad, fecha
  - `DashboardKPIs.tsx` - Tarjetas con métricas clave:
    * Total empleados activos
    * Empleados dentro de instalaciones (check-in sin check-out)
    * Total de accesos hoy
    * Alertas hoy
  - `RecentActivityFeed.tsx` - Feed de actividad reciente
  
- [x] Implementar servicio de alertas:
  ```typescript
  export const getAllAlerts = async ()
  export const getAlertsByCode = async (code)
  export const getAlertsBySeverity = async (severity)
  export const getAlertStats = async ()
  ```

- [x] Implementar gráficos de dashboard:
  - Accesos por hora del día (gráfico de líneas)
  - Alertas por tipo (gráfico de donut)
  - Top 10 empleados más activos (tabla)
  - Tendencia semanal de accesos (gráfico de área)

#### **Día 3: Reportes Avanzados (8h)**
- [x] Mejorar `AccessReportsPage.tsx`:
  - Selector de rango de fechas (date picker)
  - Export a Excel/CSV
  - Export a PDF
  - Filtros múltiples (empleado, departamento, horario)
  
- [x] Implementar componentes:
  - `DateRangePicker.tsx` - Selector de rango
  - `ExportButton.tsx` - Botón con opciones de exportación
  - `ReportTable.tsx` - Tabla avanzada con sorting y paginación
  
- [x] Implementar funcionalidades:
  - Búsqueda en tiempo real (debounced)
  - Filtros combinables
  - Ordenamiento por columna
  - Paginación server-side

#### **Día 4: UX/UI Polish (8h)**
- [x] Implementar notificaciones toast:
  - Success: "Empleado creado correctamente"
  - Error: "Error al registrar check-in"
  - Warning: "Empleado ya tiene entrada activa"
  
- [x] Implementar estados de loading:
  - Skeletons para tablas
  - Spinners para botones
  - Loading overlay para operaciones largas
  
- [x] Mejorar validaciones de formularios:
  - Validación en tiempo real
  - Mensajes de error descriptivos
  - Indicadores visuales de campos requeridos
  
- [x] Implementar confirmaciones:
  - Modal de confirmación para inactivar empleado
  - Modal de confirmación para check-out
  
- [x] Implementar dark mode (opcional pero recomendado)

#### **Día 5: Testing Frontend (4h)**
- [x] Configurar testing con Vitest + React Testing Library
- [x] Tests unitarios de componentes:
  - EmployeeForm validations
  - QuickAccessForm
  - AlertFilters
  
- [x] Tests de integración:
  - Login flow
  - CRUD employee flow
  - Access control flow
  
- [x] Configurar Cypress para E2E tests:
  - Happy path: Login → Create employee → Check-in → Check-out
  - Error handling: Invalid login, duplicate check-in

**Entregables Persona 3:**
- ✅ Dashboard completo con KPIs y gráficos
- ✅ Sistema de alertas funcional
- ✅ Reportes avanzados con exportación
- ✅ UX/UI pulido y profesional
- ✅ Tests frontend implementados

---

# 🗓️ SEMANA 3: FINALIZACIÓN Y DOCUMENTACIÓN

## **Persona 1: Optimización Final y Soporte**

### Tareas (32 horas)

#### **Día 1-2: Code Review y Refactoring (12h)**
- [x] Revisar código de SAGA Orchestrator:
  - Eliminar código duplicado
  - Mejorar nombres de variables/métodos
  - Agregar comentarios donde sea necesario
  - Verificar principios SOLID
  
- [x] Revisar código de servicios modificados:
  - Employee Service
  - Access Control Service
  
- [x] Optimizaciones de performance:
  - Revisar queries N+1 en repositorios
  - Implementar índices faltantes en BD
  - Optimizar consumo de memoria en Kafka consumers
  
- [x] Actualizar dependencias a versiones seguras:
  - Verificar vulnerabilidades con `mvn dependency:check`
  - Actualizar librerías críticas

#### **Día 3: Integración con Frontend (8h)**
- [x] Colaborar con Persona 3 para resolver issues de integración
- [x] Verificar que todos los endpoints funcionan correctamente
- [x] Ajustar respuestas de API si es necesario para frontend
- [x] Implementar endpoints faltantes si el frontend los requiere
- [x] Pruebas de integración Frontend-Backend

#### **Día 4-5: Documentación de Código y Deployment (12h)**
- [x] Agregar JavaDoc/docstrings completos:
  - Todas las clases de dominio
  - Todos los servicios
  - Todos los controladores
  
- [x] Crear **DEPLOYMENT.md**:
  - Guía paso a paso para deploy en producción
  - Configuración de variables de entorno para prod
  - Scripts de inicialización de BD
  - Configuración de Kubernetes (opcional)
  
- [x] Crear **MAINTENANCE.md**:
  - Guía de mantenimiento
  - Tareas periódicas (backups, logs, etc.)
  - Monitoreo y alertas
  - Escalamiento de servicios

**Entregables Persona 1:**
- ✅ Código refactorizado y optimizado
- ✅ Frontend-Backend integrados sin issues
- ✅ Documentación de código completa
- ✅ Guías de deployment y mantenimiento

---

## **Persona 2: Diagramas UML + Documentación Final**

### Tareas (32 horas)

#### **Día 1-2: Diagramas UML (16h)**

**1. Diagrama de Componentes** (6h)
- [x] Identificar todos los componentes:
  - Microservicios (6)
  - Bases de datos (2)
  - Event Bus (Kafka)
  - API Gateway
  - Frontend
  - Prometheus
  - Grafana
  
- [x] Definir interfaces entre componentes:
  - REST APIs
  - Kafka topics
  - Conexiones de BD
  
- [x] Herramienta: Draw.io, PlantUML, Lucidchart
- [x] Formato: PNG de alta resolución + fuente editable

**2. Diagrama de Despliegue** (6h)
- [x] Definir nodos de despliegue:
  - Contenedores Docker
  - Redes (microservices-network)
  - Volúmenes (postgres_data, mongodb_data, etc.)
  
- [x] Mostrar distribución física:
  - Puertos expuestos
  - Dependencias entre servicios
  - Health checks
  
- [x] Incluir configuración de producción (opcional):
  - Load balancers
  - Replicas
  - Auto-scaling

**3. Diagrama de Casos de Uso** (4h)
- [x] Identificar actores:
  - Administrador
  - Sistema (para alertas automáticas)
  
- [x] Definir casos de uso principales:
  - **Administrador**:
    * Iniciar sesión
    * Gestionar empleados (CRUD)
    * Registrar acceso de empleado
    * Registrar salida de empleado
    * Consultar reportes
    * Revisar alertas
  - **Sistema**:
    * Generar alerta automática
    * Ejecutar SAGA
    * Calcular duración de permanencia
  
- [x] Definir relaciones:
  - Include: Login incluido en todas las operaciones protegidas
  - Extend: Alertas extienden check-in/check-out

#### **Día 3: Documentación Final de Proyecto (8h)**
- [x] Crear **INFORME_FINAL.md**:
  
  **Sección 1: Introducción** (1h)
  - Contexto del proyecto
  - Objetivos cumplidos
  - Alcance final
  
  **Sección 2: Arquitectura** (2h)
  - Decisiones arquitectónicas
  - Justificación de tecnologías
  - Patrones implementados (SAGA, Hexagonal, DDD, EDA)
  - Diagramas UML (embebidos)
  
  **Sección 3: Implementación** (2h)
  - Descripción de cada microservicio
  - Endpoints implementados (tabla completa)
  - Modelos de datos
  - Flujos de negocio principales
  
  **Sección 4: Pruebas** (1h)
  - Estrategia de testing
  - Cobertura de tests
  - Resultados de tests E2E
  - Resultados de performance testing
  
  **Sección 5: Despliegue** (1h)
  - Instrucciones de despliegue
  - Requisitos de infraestructura
  - Configuración de monitoreo
  
  **Sección 6: Conclusiones** (1h)
  - Logros alcanzados
  - Desafíos superados
  - Mejoras futuras
  - Lecciones aprendidas

#### **Día 4-5: Presentación Final (8h)**
- [x] Crear presentación PowerPoint/Google Slides (30-40 diapositivas):
  
  **Slides:**
  1. Portada con nombre del proyecto y equipo
  2-3. Introducción y contexto
  4-5. Arquitectura de alto nivel
  6-10. Descripción de cada microservicio (1 slide por servicio)
  11-13. Diagramas UML
  14-16. SAGA Pattern explicado con diagrama de flujo
  17-19. Demostración de funcionalidades (screenshots)
  20-22. Frontend (screenshots de cada vista)
  23-25. Monitoreo y métricas (screenshots de Grafana)
  26-28. Testing y calidad
  29-30. Tecnologías utilizadas
  31-32. Desafíos y soluciones
  33-35. Demo en vivo (script de demo)
  36-37. Conclusiones
  38-40. Preguntas y respuestas
  
- [x] Preparar script de demo en vivo:
  ```
  1. Iniciar servicios con docker-compose up
  2. Mostrar dashboard de Grafana
  3. Abrir frontend
  4. Login
  5. Crear empleado
  6. Hacer check-in
  7. Mostrar alerta de check-in duplicado
  8. Hacer check-out
  9. Mostrar reporte
  10. Mostrar alertas en Alert Service
  11. Mostrar logs de SAGA Orchestrator
  12. Mostrar métricas en Prometheus
  ```
  
- [x] Crear video de demostración (5-10 min):
  - Grabación de pantalla con Loom/OBS
  - Narración explicando cada paso
  - Edición básica con transiciones

**Entregables Persona 2:**
- ✅ 3 Diagramas UML completos
- ✅ Informe final del proyecto
- ✅ Presentación profesional
- ✅ Video de demostración

---

## **Persona 3: Frontend Final + Testing UX**

### Tareas (32 horas)

#### **Día 1-2: Completar Funcionalidades Faltantes (12h)**
- [x] Implementar vista de configuración (si falta):
  - Cambiar contraseña de admin
  - Configuración de sistema (opcional)
  
- [x] Implementar búsqueda global:
  - Buscar empleados por nombre/documento
  - Buscar accesos por empleado
  - Buscar alertas por código
  
- [x] Implementar paginación en todas las tablas:
  - Empleados
  - Accesos
  - Alertas
  
- [x] Implementar filtros avanzados:
  - Empleados: activos/inactivos, búsqueda
  - Accesos: fecha, empleado, con/sin salida
  - Alertas: código, severidad, empleado, fecha
  
- [x] Implementar ordenamiento:
  - Click en headers de tabla para ordenar
  - Indicador visual de columna ordenada

#### **Día 3: Mejoras de UX (8h)**
- [x] Implementar breadcrumbs para navegación
- [x] Implementar tooltips informativos
- [x] Implementar ayuda contextual (? icons)
- [x] Mejorar mensajes de error:
  - Errores de red
  - Errores de validación
  - Errores del servidor
  
- [x] Implementar estado "offline" detection:
  - Mostrar banner si no hay conexión
  - Queue de operaciones para cuando vuelva conexión
  
- [x] Implementar auto-refresh:
  - Dashboard se actualiza cada 30 segundos
  - Notificación de nuevas alertas
  
- [x] Implementar shortcuts de teclado:
  - Ctrl+K: Búsqueda global
  - Ctrl+I: Quick check-in
  - Ctrl+O: Quick check-out

#### **Día 4: Accesibilidad y Responsive (8h)**
- [x] Verificar accesibilidad (WCAG 2.1):
  - Contraste de colores adecuado
  - Navegación por teclado
  - Screen reader friendly
  - ARIA labels
  
- [x] Mejorar responsive design:
  - Mobile: Menú hamburguesa, cards en lugar de tablas
  - Tablet: Layout optimizado
  - Desktop: Aprovechar espacio horizontal
  
- [x] Probar en diferentes navegadores:
  - Chrome
  - Firefox
  - Safari
  - Edge
  
- [x] Optimizar performance:
  - Code splitting
  - Lazy loading de rutas
  - Image optimization
  - Minimizar bundle size

#### **Día 5: Testing y Documentación Frontend (4h)**
- [x] Completar tests faltantes:
  - Todos los componentes principales
  - Todos los servicios
  - Hooks customizados
  
- [x] Verificar cobertura de tests (>70%)
- [x] Crear **FRONTEND_README.md**:
  - Estructura del proyecto
  - Componentes principales
  - Servicios y API calls
  - Guía de desarrollo
  - Scripts disponibles
  - Deployment
  
- [x] Crear guía de estilo:
  - Paleta de colores
  - Tipografía
  - Componentes reutilizables
  - Convenciones de código

**Entregables Persona 3:**
- ✅ Frontend 100% funcional
- ✅ UX pulida y profesional
- ✅ Accesible y responsive
- ✅ Tests con buena cobertura
- ✅ Documentación frontend completa

---

# 📊 Resumen de Entregables Finales

## **Código**
- ✅ SAGA Orchestrator (Spring Boot)
- ✅ API Gateway (Spring Cloud Gateway)
- ✅ Frontend (React + TypeScript)
- ✅ Tests E2E automatizados
- ✅ Scripts de prueba PowerShell

## **Documentación Técnica**
- ✅ Manual de Arquitectura
- ✅ Manual de Despliegue
- ✅ Manual de API
- ✅ Manual de Operaciones
- ✅ DEPLOYMENT.md
- ✅ MAINTENANCE.md
- ✅ FRONTEND_README.md

## **Diagramas UML**
- ✅ Diagrama de Componentes
- ✅ Diagrama de Despliegue
- ✅ Diagrama de Casos de Uso

## **Documentación de Proyecto**
- ✅ INFORME_FINAL.md
- ✅ Presentación PowerPoint (30-40 slides)
- ✅ Video de demostración (5-10 min)

## **Testing**
- ✅ Tests unitarios (>80% cobertura backend)
- ✅ Tests de integración
- ✅ Tests E2E automatizados
- ✅ Performance testing
- ✅ Tests frontend (>70% cobertura)

---

# 📅 Calendario Detallado

## Semana 1 (5 días)
| Persona | Lun | Mar | Mié | Jue | Vie |
|---------|-----|-----|-----|-----|-----|
| P1 (Backend Senior) | SAGA Setup | SAGA Setup | CheckIn SAGA | CheckOut SAGA | Testing |
| P2 (Backend/Fullstack) | Gateway Setup | Gateway Setup | Routes + Rate Limit | Integration Testing | Docs + Monitor |
| P3 (Frontend) | Project Setup | Auth + Layout | Employee CRUD | Access Control | Access Control |

## Semana 2 (5 días)
| Persona | Lun | Mar | Mié | Jue | Vie |
|---------|-----|-----|-----|-----|-----|
| P1 | Modify Services | Modify Services | SAGA Integration Tests | Optimization | Optimization |
| P2 | E2E Testing | E2E Testing | Performance Test | Tech Docs | Tech Docs |
| P3 | Alerts + Dashboard | Alerts + Dashboard | Advanced Reports | UX/UI Polish | Frontend Testing |

## Semana 3 (5 días)
| Persona | Lun | Mar | Mié | Jue | Vie |
|---------|-----|-----|-----|-----|-----|
| P1 | Code Review | Code Review | Frontend Integration | Deployment Docs | Deployment Docs |
| P2 | UML Diagrams | UML Diagrams | Final Report | Presentation | Presentation |
| P3 | Complete Features | Complete Features | UX Improvements | Accessibility + Responsive | Frontend Docs |

---

# 🎯 KPIs y Métricas de Éxito

## **Cobertura de Funcionalidades**
- ✅ 100% de requisitos funcionales implementados
- ✅ 100% de endpoints según contexto.MD
- ✅ 100% de alertas configuradas

## **Calidad de Código**
- ✅ Cobertura de tests backend >80%
- ✅ Cobertura de tests frontend >70%
- ✅ 0 vulnerabilidades críticas
- ✅ Code smells <50 (SonarQube)

## **Performance**
- ✅ Tiempo de respuesta promedio <500ms
- ✅ Soporta 100 usuarios concurrentes
- ✅ 99% uptime en tests de carga

## **Documentación**
- ✅ Todos los servicios documentados
- ✅ Todos los endpoints en Swagger
- ✅ 3 Diagramas UML completos
- ✅ Manuales técnicos completos

---

# 🚀 Reuniones de Sincronización

## **Daily Standup (15 min)**
- **Horario**: Todos los días a las 9:00 AM
- **Formato**:
  - ¿Qué hice ayer?
  - ¿Qué haré hoy?
  - ¿Tengo bloqueadores?

## **Weekly Review (1 hora)**
- **Horario**: Viernes a las 4:00 PM
- **Agenda**:
  - Demo de lo completado
  - Retrospectiva
  - Planificación de próxima semana

## **Final Presentation (2 horas)**
- **Fecha**: Último día de Semana 3
- **Formato**:
  - Presentación PowerPoint
  - Demo en vivo
  - Q&A

---

# 📝 Notas Importantes

## **Prioridades**
1. **Alta**: SAGA Orchestrator, API Gateway (bloqueadores para frontend)
2. **Media**: Frontend funcional, Tests E2E
3. **Baja**: Optimizaciones, documentación adicional

## **Riesgos Identificados**
- ⚠️ Integración SAGA puede tomar más tiempo del estimado
- ⚠️ API Gateway puede tener issues de configuración
- ⚠️ Frontend puede necesitar ajustes de UX

## **Mitigaciones**
- ✅ Buffer de 10% en estimaciones
- ✅ Code reviews diarios
- ✅ Testing continuo desde día 1

---

# 🎓 Entregables Académicos (Parte A - contexto.MD)

Al finalizar las 3 semanas, se tendrá:

## **Vista de Despliegue**
- ✅ Diagrama de Componentes UML

## **Vista Física**
- ✅ Diagrama de Despliegue UML

## **Escenarios**
- ✅ Diagrama de Casos de Uso UML

## **Parte B - Desarrollo de la Solución**
- ✅ Sistema completamente funcional
- ✅ Demo preparada para sustentación

## **Parte C - Documentación APIs**
- ✅ Swagger para todos los microservicios
- ✅ Manual consolidado de APIs

---

**¡Éxito en el desarrollo! 🚀**
