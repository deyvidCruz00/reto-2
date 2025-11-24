import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Employee, EmployeeResponse } from '../models/employee.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {
  private apiUrl = `${environment.apiUrl}${environment.endpoints.employee}`;

  constructor(private http: HttpClient) {}

  // Crear empleado
  createEmployee(employee: Omit<Employee, 'documentNumber'> & { document: string }): Observable<EmployeeResponse> {
    return this.http.post<EmployeeResponse>(`${this.apiUrl}/createemployee`, employee);
  }

  // Actualizar empleado
  updateEmployee(employee: Partial<Employee> & { document: string }): Observable<EmployeeResponse> {
    return this.http.put<EmployeeResponse>(`${this.apiUrl}/updateemployee`, employee);
  }

  // Obtener todos los empleados
  getAllEmployees(): Observable<EmployeeResponse> {
    return this.http.get<EmployeeResponse>(`${this.apiUrl}/findallemployees`);
  }

  // Buscar empleado por documento
  getEmployeeByDocument(document: string): Observable<EmployeeResponse> {
    return this.http.get<EmployeeResponse>(`${this.apiUrl}/findemployee/${document}`);
  }

  // Inactivar empleado
  disableEmployee(document: string): Observable<EmployeeResponse> {
    return this.http.put<EmployeeResponse>(`${this.apiUrl}/disableemployee/${document}`, {});
  }

  // Health check
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/actuator/health`);
  }
}
