import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Access, AccessResponse, AccessReport } from '../models/access.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AccessService {
  private apiUrl = `${environment.apiUrl}${environment.endpoints.access}`;

  constructor(private http: HttpClient) {}

  // Registrar entrada (check-in)
  checkIn(employeeDocument: string): Observable<AccessResponse> {
    return this.http.post<AccessResponse>(`${this.apiUrl}/usercheckin`, {
      employeeDocumentNumber: employeeDocument
    });
  }

  // Registrar salida (check-out)
  checkOut(employeeDocument: string): Observable<AccessResponse> {
    return this.http.post<AccessResponse>(`${this.apiUrl}/usercheckout`, {
      employeeDocumentNumber: employeeDocument
    });
  }

  // Obtener todos los registros de acceso
  getAllAccess(): Observable<AccessResponse> {
    return this.http.get<AccessResponse>(`${this.apiUrl}/all`);
  }

  // Obtener accesos activos de un empleado
  getActiveAccessByEmployee(employeeDocument: string): Observable<AccessResponse> {
    return this.http.get<AccessResponse>(`${this.apiUrl}/employee/${employeeDocument}/active`);
  }

  // Reporte de empleados por fecha
  getEmployeesByDate(date: string): Observable<{success: boolean; data: AccessReport[]}> {
    return this.http.get<{success: boolean; data: AccessReport[]}>(`${this.apiUrl}/allemployeesbydate`, {
      params: { date }
    });
  }

  // Reporte de accesos de un empleado por rango de fechas
  getEmployeeByDateRange(employeeDocument: string, startDate: string, endDate: string): Observable<AccessResponse> {
    return this.http.get<AccessResponse>(`${this.apiUrl}/employeebydates`, {
      params: {
        employeeDocument,
        startDate,
        endDate
      }
    });
  }

  // Health check
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/actuator/health`);
  }
}
