import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Alert, AlertResponse, AlertCode } from '../models/alert.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private apiUrl = `${environment.apiUrl}${environment.endpoints.alert}`;

  constructor(private http: HttpClient) {}

  // Obtener todas las alertas
  getAllAlerts(): Observable<AlertResponse> {
    return this.http.get<AlertResponse>(`${this.apiUrl}/all`);
  }

  // Obtener alertas pendientes (no resueltas)
  getPendingAlerts(): Observable<AlertResponse> {
    return this.http.get<AlertResponse>(`${this.apiUrl}/pending`);
  }

  // Resolver una alerta
  resolveAlert(alertId: string): Observable<AlertResponse> {
    return this.http.put<AlertResponse>(`${this.apiUrl}/resolve/${alertId}`, {});
  }

  // Crear alerta manualmente
  createAlert(alert: Partial<Alert>): Observable<AlertResponse> {
    return this.http.post<AlertResponse>(`${this.apiUrl}/create`, alert);
  }

  // Health check
  checkHealth(): Observable<any> {
    return this.http.get(`${this.apiUrl}/actuator/health`);
  }
}
