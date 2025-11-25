// Modelo de Registro de Acceso
export interface Access {
  id?: string;                     // ID del registro
  employeeId: string;              // ID/Documento del empleado
  accessDatetime: string;          // Fecha y hora de entrada (ISO format)
  exitDatetime?: string;           // Fecha y hora de salida (ISO format, opcional)
  durationMinutes?: number;        // Duración en minutos (opcional)
}

// Respuesta del servidor
export interface AccessResponse {
  success: boolean;
  message?: string;
  data?: Access | Access[];
}

// Reporte de acceso por fecha
export interface AccessReport {
  id?: string;
  employeeId: string;
  accessDatetime: string;
  exitDatetime?: string;
  durationMinutes?: number;
}
