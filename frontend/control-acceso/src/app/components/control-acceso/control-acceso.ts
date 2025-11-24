import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { EmployeeService } from '../../services/employee.service';
import { AccessService } from '../../services/access.service';
import { Employee } from '../../models/employee.model';
import { Access } from '../../models/access.model';

@Component({
  selector: 'app-control-acceso',
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatChipsModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSnackBarModule
  ],
  templateUrl: './control-acceso.html',
  styleUrl: './control-acceso.scss',
})
export class ControlAcceso implements OnInit {
  documentNumber = '';
  selectedEmployee = signal<Employee | null>(null);
  searchPerformed = signal(false);
  processingAccess = signal(false);
  
  employeesInside = signal(0);
  employeesInsideList = signal<Access[]>([]);
  
  accessHistory = signal<Access[]>([]);
  loadingHistory = signal(false);
  
  dateStart: Date = new Date();
  dateEnd: Date = new Date();
  
  historyColumns = ['documentNumber', 'entry', 'exit', 'duration'];

  constructor(
    private employeeService: EmployeeService,
    private accessService: AccessService,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEmployeesInside();
    this.loadAccessHistory();
  }

  searchEmployee(): void {
    if (!this.documentNumber.trim()) {
      return;
    }

    this.searchPerformed.set(true);
    this.employeeService.getAllEmployees().subscribe({
      next: (response) => {
        const employees = Array.isArray(response.data) ? response.data : [];
        const employee = employees.find(
          (e: any) => e.documentNumber === this.documentNumber.trim()
        );
        this.selectedEmployee.set(employee || null);
        
        if (!employee) {
          this.showMessage('Empleado no encontrado', 'error');
        }
      },
      error: (err) => {
        console.error('Error buscando empleado:', err);
        this.showMessage('Error buscando empleado', 'error');
      }
    });
  }

  checkIn(): void {
    const employee = this.selectedEmployee();
    if (!employee) return;

    this.processingAccess.set(true);
    this.accessService.checkIn(employee.documentNumber).subscribe({
      next: () => {
        this.showMessage('Entrada registrada exitosamente', 'success');
        this.resetForm();
        this.loadEmployeesInside();
        this.loadAccessHistory();
        this.processingAccess.set(false);
      },
      error: (err) => {
        console.error('Error registrando entrada:', err);
        this.showMessage(err.error?.message || 'Error registrando entrada', 'error');
        this.processingAccess.set(false);
      }
    });
  }

  checkOut(): void {
    const employee = this.selectedEmployee();
    if (!employee) return;

    this.processingAccess.set(true);
    this.accessService.checkOut(employee.documentNumber).subscribe({
      next: () => {
        this.showMessage('Salida registrada exitosamente', 'success');
        this.resetForm();
        this.loadEmployeesInside();
        this.loadAccessHistory();
        this.processingAccess.set(false);
      },
      error: (err) => {
        console.error('Error registrando salida:', err);
        this.showMessage(err.error?.message || 'Error registrando salida', 'error');
        this.processingAccess.set(false);
      }
    });
  }

  loadEmployeesInside(): void {
    this.accessService.getAllAccess().subscribe({
      next: (response) => {
        const accesses = Array.isArray(response.data) ? response.data : [];
        const inside = accesses.filter((a: any) => !a.exit_datetime);
        this.employeesInsideList.set(inside);
        this.employeesInside.set(inside.length);
      },
      error: (err) => console.error('Error cargando empleados dentro:', err)
    });
  }

  loadAccessHistory(): void {
    this.loadingHistory.set(true);
    const start = this.formatDate(this.dateStart);
    const end = this.formatDate(this.dateEnd);

    this.accessService.getEmployeesByDate(start).subscribe({
      next: (response) => {
        const accesses = Array.isArray(response.data) ? response.data : [];
        this.accessHistory.set(accesses as any);
        this.loadingHistory.set(false);
      },
      error: (err) => {
        console.error('Error cargando historial:', err);
        this.loadingHistory.set(false);
      }
    });
  }

  resetForm(): void {
    this.documentNumber = '';
    this.selectedEmployee.set(null);
    this.searchPerformed.set(false);
  }

  formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
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

  formatTime(dateTimeStr: string): string {
    const date = new Date(dateTimeStr);
    return date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  calculateDuration(entry: string, exit?: string): string {
    if (!exit) return '-';
    
    const entryDate = new Date(entry);
    const exitDate = new Date(exit);
    const diff = exitDate.getTime() - entryDate.getTime();
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${hours}h ${minutes}m`;
  }

  showMessage(message: string, type: 'success' | 'error'): void {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      panelClass: type === 'success' ? 'success-snackbar' : 'error-snackbar'
    });
  }
}
