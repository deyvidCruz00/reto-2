// Modelo de Registro de Acceso
export interface Access {
  employeeDocumentNumber: string;  // Documento del empleado
  entry_datetime: string;          // Fecha y hora de entrada
  exit_datetime?: string;          // Fecha y hora de salida (opcional)
}

// Respuesta del servidor
export interface AccessResponse {
  success: boolean;
  message?: string;
  data: Access | Access[];
}

// Reporte de acceso por fecha
export interface AccessReport {
  employeeDocumentNumber: string;
  employeeName: string;
  entryTime: string;
  exitTime: string;
  duration: string;
}
