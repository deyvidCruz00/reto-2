// Modelo de Empleado
export interface Employee {
  documentNumber: string;    // Documento de identidad
  firstName: string;         // Nombre
  lastName: string;          // Apellido
  email: string;             // Correo electrónico
  phoneNumber: string;       // Teléfono
  status: boolean;           // Estado (true=activo, false=inactivo)
}

// Respuesta del servidor
export interface EmployeeResponse {
  success: boolean;
  message?: string;
  data: Employee | Employee[];
}
