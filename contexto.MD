**UNIVERSIDAD PEDAGÓGICA Y TECNOLÓGICA DE COLOMBIA**

**FACULTAD DE INGENIERÍA**

**ESCUELA DE INGENIERÍA DE SISTEMAS**

**RETO SEGUNDO CORTE - INGENIERÍA DE SOFTWARE II**

**OBJETIVO**

Aplicar los conocimientos adquiridos con respecto a las arquitecturas de software (Arquitectura EDA, CQRS, SAGA, Service Mesh, DDD y Hexagonal) en un proyecto práctico bajo diferentes plataformas tecnológicas.

**PREREQUISITOS DEL PROYECTO**

Para el presente proyecto vamos a requerir al menos las siguientes tecnologías:

- Frontend (A elegir por el grupo)
- ORM (Para aplicar la arquitectura DTO con JPA, a elegir)
- Event Bus: Kafka o RabbitMQ (U otra tecnología a elegir)
- Motores de base de datos (Ver arquitectura de la solución):
  - Base de datos relacional (a elegir)
  - Base de datos NoSQL (a elegir)
- Tecnologías de monitorización de servicios: Prometheus y Grafana.
- Otras tecnologías (a elegir)

**PROPÓSITO DEL PROYECTO**

El presente proyecto tiene como propósito la realización de sistema de información que maneje el proceso de registrar usuarios, empleados y gestionar accesos a las instalaciones de una empresa.

**DESCRIPCIÓN DEL PROYECTO**

Se requiere construir un sistema de información para el control de acceso peatonal a las instalaciones de una empresa. Dado que la empresa tiene clientes en todo el país se tomó la decisión de realizar un sistema bajo la arquitectura bajo microservicios en conjunto con la arquitectura DTO para poder manejar la persistencia de los datos requeridos por el sistema. Por lo anterior se identifica que se requieren manejar los siguientes requisitos funcionales:

- _Login_
  - Registrar usuario del sistema: Aquí se registra el ID del usuario y su contraseña. Solo hay un tipo de rol para este fin, que será el de _administrador_. **_Con respecto a esta funcionalidad no va a estar disponible desde el frontend solo a través del microservicio desde su endpoint._**
  - Autenticar usuario del sistema: Si el usuario es un usuario válido y tuvo más de 3 intentos fallidos se debe bloquear su acceso por 10 minutos.
- _Gestión de empleados_
  - Registrar empleado: Esto involucra registrar el documento de identidad, nombre, apellidos, email, número de celular y el estado del empleado (activo e inactivo).
  - Editar empleado: Se pueden modificar todos los datos del empleado menos su documento de identidad.
  - Mostrar todos empleados: Permite ver todos los empleados que están registrados en el sistema, sin importar su estado. Puede incluir el acceso directo a modificar un empleado o registrar uno nuevo.
  - Inactivar un empleado: Involucra cambiar el estado de activo a inactivo. Este campo es de tipo boolean que implica que false es inactivo y true es activo.

Nota: La funcionalidad de eliminar un empleado no se incluye dado que no existe la eliminación de registros de la base de datos en este sistema, solo su inactivación.

- _Gestión de accesos_
  - Registrar acceso de un empleado a las instalaciones: Esto involucra registrar la fecha y hora de entrada a las instalaciones (hora actual del sistema) y el ID del empleado. El sistema debería controlar que un usuario que ya ha realizado su acceso no lo intente de nuevo.
  - Registrar salida de un empleado a las instalaciones: Esto involucra registrar la fecha y hora de salida de las instalaciones (hora actual del sistema) y el ID del empleado. El sistema debería controlar que un usuario que ya ha realizado su salida no lo intente de nuevo.
- _Registrar alertas_
  - Registrar alertas: El sistema deberá registrar alertas en las siguientes situaciones:
    - Cuando un usuario no registrado trata de realizar login 2 veces: Debe almacenarse la hora del intento y el usuario con que trataron de generar el acceso. Adicionalmente se debe colocar un código de alerta como "LOGIN_USR_NOT_REGISTERED".
    - Cuando un usuario registrado tiene más de 3 intentos fallidos en su login: Debe almacenarse la hora del intento, el usuario con que trataron de generar el acceso. Adicionalmente se debe colocar un código de alerta como "LOGIN_USR_ATTEMPS_EXCEEDED".
    - Cuando un empleado que ya ha realizado un ingreso previo a las instalaciones (sin generar salida) trata de ingresar de nuevo. Debe almacenarse la hora del intento, el usuario con que trataron de generar el acceso. Adicionalmente se debe colocar un código de alerta como "EMPLOYEE_ALREADY_ENTERED".
    - Cuando un empleado que ya ha realizado una salida previa (sin generar salida) trata de ingresar de nuevo. Debe almacenarse la hora del intento, el usuario con que trataron de generar el acceso. Adicionalmente se debe colocar un código de alerta como "EMPLOYEE_ALREADY_LEFT".
- _Reportes del sistema_
  - Generar un reporte de los empleados que han accedido en una fecha: Este reporte debe contener el documento de identidad del empleado, la hora de entrada a la instalación y la hora de salida de la instalación y la duración (expresada en horas y minutos)
  - Generar un reporte de un empleado específico: Este reporte debe solicitar el documento del empleado, la fecha de inicio del reporte, la fecha de fin de reporte y con esta información deberá generar el reporte de todos los ingresos de cada empleado.

**ESTRUCTURA DEL SISTEMA**

El sistema debe contar con la siguiente estructura:

- Debe desarrollarse una aplicación web para que el administrador pueda ejecutar sus funcionalidades, descritas en los requisitos funcionales anteriores.
- Debe configurarse las herramientas para soportar la solución (Bases de datos, pruebas, rendimiento, monitoreo, eventos, etc).

**DEFINICIONES DE PLATAFORMA TECNOLÓGICA**

Las siguientes consideraciones se deben tener en cuenta para el desarrollo del proyecto:

- El proyecto de la aplicación será implementado bajo las tecnologías que requieran. Se recomienda partir de VSCode y SpringBoot
- Los requisitos funcionales deben ser desarrollados bajo los siguientes estilos arquitectónicos y arquitecturas modernas:
  - Arquitecturas por microservicios para cada una de las funcionalidades descritas
  - Event-Driven Architecture (EDA)
  - Puede elegir para mantener la consistencia entre los microservicios y para asegurar procesos E2E como el de registrar acceso debe consultar que el usuario exista para darle acceso al sistema o que el empleado exista para realizar el acceso al sistema se recomienda implementar alguno
    - Arquitectura SAGA
    - Service Mesh
  - CQRS (Opcional)
  - Domain-Driven Design (DDD)
  - Arquitectura hexagonal
- Debe contar con un método de autenticación basado en esquema basado en Tokens y que tenga autenticación multifactor. La información del usuario y contraseña deben estar almacenada en la BD LoginDB.
- El manejo de información de la gestión de usuarios debe persistir bajo una instancia NoSQL.
- El manejo de la información de los clientes del sistema debe persistir en un modelo relacional.
- La persistencia del proyecto debe estar administrada bajo JPA (Relacional y No relacional).
- Se debe considerar implementar un event bus para exponer los microservicios tanto a otros microservicios como a los usuarios.
- Se debe considerar implementar monitoreo de los microservicios y de las transacciones del sistema en general.

**ATRIBUTOS DE CALIDAD**

Los siguientes son los atributos de calidad del sistema que se deben considerar en su implementación:

**SEGURIDAD**

Con respecto al requisito no funcional de seguridad se debe considerar implementar una solución de autenticación bajo un servicio de Token y que permita autenticación multifactor.

**MONITOREO**

Después de desplegar un servicio o una aplicación, debemos de saber todo lo que sucede en este mismo, pues si llegase a fallar por situaciones desconocidas, tenemos que estar informados y estar conscientes de que hay un error para posteriormente solucionarlo cuanto antes y así evitar que los usuarios que consumen esta aplicación tengan dificultades para acceder a ella.

Para monitorear nuestros servicios utilizaremos Prometheus con Grafana. Prometheus es una base de series de tiempo y un sistema de monitoreo y alertas. Por su parte Grafana es la plataforma de análisis para métricas, que le permite consultar, visualizar, alertar y comprender los datos, sin importar dónde estén almacenadas. Le permite crear, explorar y compartir tableros de control con su equipo. Sin embargo, si requieren el uso de otras tecnologías para monitoreo las pueden implementar

**PERSISTENCIA**

Los siguientes son los requisitos a considerar en la persistencia de la solución:

- Implementar la arquitectura DTO para poder interconectar el ORM que se adapte al lenguaje de programación y que trabaje con la base de datos relacional desde el lenguaje de programación seleccionado por ustedes.
- Implementar la arquitectura DTO para poder interconectar el ORM al lenguaje de programación y que trabaje con la base de datos No relacional desde el lenguaje de programación seleccionado por ustedes.

**ESTRUCTURA DE DATOS DE LA PERSISTENCIA**

La siguiente debe ser la estructura de datos que debe tener la persistencia en cada una de las bases de datos:

**LOGIN**

- Nombre de la Base de datos: LoginDB
- Nombre de la tabla: Login

| Nombre del campo | Tabla | Tipo/Tamaño de dato | Requerimientos adicionales |
| --- | --- | --- | --- |
| id  | Login | SERIAL (Autoincrement) | PRIMARY KEY, Not Null |
| userID | Login | BIGINTEGER | Not Null |
| password | Login | VARCHAR (20) | Not Null |

**EMPLOYEE:**

- Nombre de la Base de datos: EmployeeDB
- Nombre de la tabla: Employee

| Nombre del campo | Tabla | Tipo/Tamaño de dato |
| --- | --- | --- |
| document | Employee | Strings |
| firstname | Employee | Strings |
| lastname | Employee | Strings |
| email | Employee | Strings |
| phone | Employee | Strings |
| status | Employee | Boolean |

**ACCESS CONTROL:**

- Nombre de la Base de datos: AccessControlDB
- Nombre de la tabla: Access

| Nombre del campo | Tabla | Tipo/Tamaño de dato |
| --- | --- | --- |
| employeeID (Employee document) | Access | String |
| accessdatetime | Access | String |

**ALERTS:**

- Nombre de la Base de datos: AccessControlDB
- Nombre de la tabla: Alert

| Nombre del campo | Tabla | Tipo/Tamaño de dato |
| --- | --- | --- |
| ID  | Alert | Strings |
| Timestamp | Alert | Strings/Date |
| Description | Alert | Strings |
| Code | Employee | Strings |

**NOMBRECLATURA PARA EL LLAMADO DE LOS MICROSERVICIOS**

Por favor consideren los siguientes RequestMapping para cada uno de los microservicios que se van a exponer de acuerdo a la siguiente lista:

| Funcionalidad | Request Mapping | Microservicio | GetMapping / PostMapping |
| --- | --- | --- | --- |
| Login | login | Registrar usuario | Createuser |
| Login | login | Autenticar Usuario | Authuser |
| Employee | employee | Crear empleado | Createemployee |
| Employee | employee | Modificar empleado | updateemployee |
| Employee | employee | Buscar todos los empleados | findallemployees |
| Employee | employee | Inactivar empleado | disableemployee |
| Access control | access | Registrar ingreso del usuario a las instalaciones | usercheckin |
| Access control | access | Registrar salida del usuario de las instalaciones | usercheckout |
| Access control | access | Reporte empleados registrados por fecha | allemployeesbydate |
| Access control | access | Reporte accesos por empleado por rangos de fecha | employeebydates |
| Alert | alert | Intento de autenticación de un usuario que no existe al menos 2 veces | Usrnotregistattempt |
| Alert | alert | Intento de autenticación de un usuario registrado más de 3 veces | Usrexceedattempts |
| Alert | alert | Intento de ingreso de un empleado que aparece con ingreso activo | employeealreadyentered |
| Alert | alert | Intento de salida de un empleado que aparece que salió en el sistema | employeealreadyleft |

**DINÁMICA DEL PROYECTO**

El proyecto se tiene contemplado realizarse en dos avances hasta llegar al sistema completado en su funcionalidad. Para cada avance se solicitará cumplir con una etapa del proyecto, la cual se representará en un entregable.

**ACTIVIDADES DEL PROYECTO**

En sus grupos de proyecto desarrollar el diseño arquitectónico que incluye lo siguiente:

**PARTE A. MODELO DE LA ARQUITECTURA DE LA SOLUCIÓN (SEMANA 15)**

Se debe generar la arquitectura de la solución. Para esto se requiere entregar los siguientes diagramas basados en algunas de las vistas de la implementación de la arquitectura de 4+1 vistas de Phillipe Kruchten:

- Vista de despliegue:
  - Diagrama de componentes UML: Debe contener los diferentes componentes de la solución.
- Vista física:
  - Diagrama de despliegue UML: Contiene la descripción física de la arquitectura en la cual se complementa el diagrama de arquitectura física incluyendo la distribución de los componentes en cada uno de los nodos.
- Escenarios
  - Diagrama de casos de uso UML

Este documento debe ser entregado en el link denominado "Primera entrega - Modelo de la arquitectura de la solución" disponible en el aula virtual:


**PARTE B: DESARROLLO DE LA SOLUCIÓN (SEMANA 17)**

En la sustentación final se deberá mostrar la solución implementada explicando la estructura del proyecto (carpetas, distintos tipos de código fuente como controllers, services, configurations, repositories, value objects, user cases, etc). De igual manera se solicitará realizar un demo para tal fin.

**PARTE C: DOCUMENTACION APIS**

Para la presentación de los microservicios que harán parte del proyecto se deben documentar mediante un API que facilite su acceso, tales como Swagger. Para la prueba de los microservicios sigan los estándares definidos para la creación de los API.

**FORMA DE ENTREGA**

Este primer avance se debe documentar en formato Word la parte A de la solución y entregarla para revisión el próximo martes 11 de noviembre. Para poder continuar con el proyecto es indispensable que esta parte sea aprobada.

La sustentación será en la semana 17 (martes 25 de noviembre).