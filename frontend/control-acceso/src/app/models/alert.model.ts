// Tipos de alerta del sistema
export enum AlertCode {
  LOGIN_USER_NOT_REGISTERED = 'LOGIN_USR_NOT_REGISTERED',
  LOGIN_ATTEMPTS_EXCEEDED = 'LOGIN_USR_ATTEMPS_EXCEEDED',
  EMPLOYEE_ALREADY_ENTERED = 'EMPLOYEE_ALREADY_ENTERED',
  EMPLOYEE_ALREADY_LEFT = 'EMPLOYEE_ALREADY_LEFT'
}

// Severidad de la alerta
export enum AlertSeverity {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
  CRITICAL = 'CRITICAL'
}

// Modelo de Alerta
export interface Alert {
  id: string;
  timestamp: string;
  description: string;
  code: AlertCode | string;
  severity?: AlertSeverity;
  resolved: boolean;
  resolvedAt?: string;
}

// Respuesta del servidor
export interface AlertResponse {
  success: boolean;
  message?: string;
  data: Alert | Alert[];
}
