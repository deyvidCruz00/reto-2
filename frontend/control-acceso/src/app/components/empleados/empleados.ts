import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { EmployeeService } from '../../services/employee.service';
import { Employee } from '../../models/employee.model';
import { EmployeeDialogComponent } from './employee-dialog.component';

@Component({
  selector: 'app-empleados',
  imports: [
    CommonModule,
    FormsModule,
    MatCardModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
    MatDialogModule,
    MatSnackBarModule
  ],
  templateUrl: './empleados.html',
  styleUrl: './empleados.scss',
})
export class Empleados implements OnInit {
  employees = signal<Employee[]>([]);
  filteredEmployees = signal<Employee[]>([]);
  loading = signal(true);
  
  searchText = '';
  statusFilter = 'all';
  
  displayedColumns: string[] = ['documentNumber', 'fullName', 'email', 'phoneNumber', 'status', 'actions'];

  constructor(
    private employeeService: EmployeeService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadEmployees();
  }

  loadEmployees(): void {
    this.loading.set(true);
    this.employeeService.getAllEmployees().subscribe({
      next: (response) => {
        const employees = Array.isArray(response.data) ? response.data : [];
        this.employees.set(employees);
        this.applyFilter();
        this.loading.set(false);
      },
      error: (err) => {
        console.error('Error cargando empleados:', err);
        this.loading.set(false);
        this.showMessage('Error cargando empleados', 'error');
      }
    });
  }

  applyFilter(): void {
    let filtered = this.employees();
    
    // Filtro por texto
    if (this.searchText) {
      const search = this.searchText.toLowerCase();
      filtered = filtered.filter(e =>
        e.documentNumber.toLowerCase().includes(search) ||
        e.firstName.toLowerCase().includes(search) ||
        e.lastName.toLowerCase().includes(search) ||
        e.email.toLowerCase().includes(search) ||
        e.phoneNumber.toLowerCase().includes(search)
      );
    }
    
    // Filtro por estado
    if (this.statusFilter !== 'all') {
      filtered = filtered.filter(e => 
        this.statusFilter === 'active' ? e.status : !e.status
      );
    }
    
    this.filteredEmployees.set(filtered);
  }

  openEmployeeDialog(employee?: Employee): void {
    const dialogRef = this.dialog.open(EmployeeDialogComponent, {
      width: '600px',
      data: employee ? { ...employee } : null
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        if (employee) {
          this.updateEmployee(result);
        } else {
          this.createEmployee(result);
        }
      }
    });
  }

  createEmployee(employee: Employee): void {
    const employeeData = { ...employee, document: employee.documentNumber };
    this.employeeService.createEmployee(employeeData as any).subscribe({
      next: () => {
        this.showMessage('Empleado creado exitosamente', 'success');
        this.loadEmployees();
      },
      error: (err) => {
        console.error('Error creando empleado:', err);
        this.showMessage('Error creando empleado', 'error');
      }
    });
  }

  updateEmployee(employee: Employee): void {
    const employeeData = { ...employee, document: employee.documentNumber };
    this.employeeService.updateEmployee(employeeData as any).subscribe({
      next: () => {
        this.showMessage('Empleado actualizado exitosamente', 'success');
        this.loadEmployees();
      },
      error: (err) => {
        console.error('Error actualizando empleado:', err);
        this.showMessage('Error actualizando empleado', 'error');
      }
    });
  }

  toggleEmployeeStatus(employee: Employee): void {
    if (employee.status) {
      this.employeeService.disableEmployee(employee.documentNumber).subscribe({
        next: () => {
          this.showMessage('Empleado desactivado exitosamente', 'success');
          this.loadEmployees();
        },
        error: (err) => {
          console.error('Error desactivando empleado:', err);
          this.showMessage('Error desactivando empleado', 'error');
        }
      });
    } else {
      // Para activar, actualizamos el empleado con status true
      this.employeeService.updateEmployee({ ...employee, status: true, document: employee.documentNumber } as any).subscribe({
        next: () => {
          this.showMessage('Empleado activado exitosamente', 'success');
          this.loadEmployees();
        },
        error: (err) => {
          console.error('Error activando empleado:', err);
          this.showMessage('Error activando empleado', 'error');
        }
      });
    }
  }

  showMessage(message: string, type: 'success' | 'error'): void {
    this.snackBar.open(message, 'Cerrar', {
      duration: 3000,
      panelClass: type === 'success' ? 'success-snackbar' : 'error-snackbar'
    });
  }
}
