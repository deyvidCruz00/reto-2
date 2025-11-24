import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { EmployeeService } from '../../services/employee.service';
import { AccessService } from '../../services/access.service';
import { AlertService } from '../../services/alert.service';
import { Access } from '../../models/access.model';
import { Alert } from '../../models/alert.model';

interface DashboardStats {
  totalEmployees: number;
  activeEmployees: number;
  employeesInside: number;
  todayAccess: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [
    CommonModule,
    MatCardModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatTooltipModule
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  stats = signal<DashboardStats>({
    totalEmployees: 0,
    activeEmployees: 0,
    employeesInside: 0,
    todayAccess: 0
  });
  
  recentAccess = signal<Access[]>([]);
  pendingAlerts = signal<Alert[]>([]);
  loading = signal(true);

  constructor(
    private employeeService: EmployeeService,
    private accessService: AccessService,
    private alertService: AlertService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading.set(true);

    // Cargar empleados
    this.employeeService.getAllEmployees().subscribe({
      next: (response) => {
        const employees = Array.isArray(response.data) ? response.data : [];
        const total = employees.length || 0;
        const active = employees.filter((e: any) => e.status).length || 0;
        this.stats.update(s => ({ ...s, totalEmployees: total, activeEmployees: active }));
      },
      error: (error) => console.error('Error loading employees:', error)
    });

    // Cargar accesos de hoy
    const today = new Date().toISOString().split('T')[0];
    this.accessService.getEmployeesByDate(today).subscribe({
      next: (response) => {
        const accesses = Array.isArray(response.data) ? response.data : [];
        this.recentAccess.set(accesses.slice(0, 10) as any); // Últimos 10
        this.stats.update(s => ({ ...s, todayAccess: accesses.length }));
        
        // Calcular empleados dentro (entrada sin salida)
        const inside = accesses.filter((a: any) => !a.exit_datetime).length;
        this.stats.update(s => ({ ...s, employeesInside: inside }));
        
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error cargando accesos:', err);
        this.loading.set(false);
      }
    });

    // Cargar alertas pendientes
    this.alertService.getPendingAlerts().subscribe({
      next: (response) => {
        const alerts = Array.isArray(response.data) ? response.data : [];
        this.pendingAlerts.set(alerts);
      },
      error: (err) => console.error('Error cargando alertas:', err)
    });
  }

  formatDateTime(dateTimeStr: string): string {
    const date = new Date(dateTimeStr);
    return date.toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  formatAlertCode(code: string): string {
    return code.replace(/_/g, ' ');
  }

  getAlertIcon(code: string): string {
    if (code.includes('LOGIN')) return 'lock';
    if (code.includes('EMPLOYEE')) return 'person';
    return 'warning';
  }

  resolveAlert(id: string): void {
    this.alertService.resolveAlert(id).subscribe({
      next: () => {
        this.pendingAlerts.update(alerts => alerts.filter(a => a.id !== id));
      },
      error: (err) => console.error('Error resolviendo alerta:', err)
    });
  }
}
