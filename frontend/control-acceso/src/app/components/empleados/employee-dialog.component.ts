import { Component, Inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { Employee } from '../../models/employee.model';

@Component({
  selector: 'app-employee-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCheckboxModule
  ],
  template: `
    <h2 mat-dialog-title>{{ data ? 'Editar Empleado' : 'Nuevo Empleado' }}</h2>
    <form [formGroup]="employeeForm" (ngSubmit)="onSubmit()">
      <mat-dialog-content>
        <div class="form-grid">
          <mat-form-field appearance="outline">
            <mat-label>N\u00famero de Documento</mat-label>
            <input matInput formControlName="documentNumber" [readonly]="!!data" required>
            @if (employeeForm.get('documentNumber')?.hasError('required')) {
              <mat-error>El documento es requerido</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Nombres</mat-label>
            <input matInput formControlName="firstName" required>
            @if (employeeForm.get('firstName')?.hasError('required')) {
              <mat-error>Los nombres son requeridos</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Apellidos</mat-label>
            <input matInput formControlName="lastName" required>
            @if (employeeForm.get('lastName')?.hasError('required')) {
              <mat-error>Los apellidos son requeridos</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Email</mat-label>
            <input matInput formControlName="email" type="email" required>
            @if (employeeForm.get('email')?.hasError('required')) {
              <mat-error>El email es requerido</mat-error>
            }
            @if (employeeForm.get('email')?.hasError('email')) {
              <mat-error>Email inv\u00e1lido</mat-error>
            }
          </mat-form-field>

          <mat-form-field appearance="outline">
            <mat-label>Tel\u00e9fono</mat-label>
            <input matInput formControlName="phoneNumber" required>
            @if (employeeForm.get('phoneNumber')?.hasError('required')) {
              <mat-error>El tel\u00e9fono es requerido</mat-error>
            }
          </mat-form-field>

          <div class="checkbox-container">
            <mat-checkbox formControlName="status">Activo</mat-checkbox>
          </div>
        </div>
      </mat-dialog-content>

      <mat-dialog-actions align="end">
        <button mat-button type="button" (click)="onCancel()">Cancelar</button>
        <button mat-raised-button color="primary" type="submit" [disabled]="!employeeForm.valid">
          {{ data ? 'Actualizar' : 'Crear' }}
        </button>
      </mat-dialog-actions>
    </form>
  `,
  styles: [`
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      padding: 16px 0;
      
      mat-form-field {
        width: 100%;
      }
      
      mat-form-field:first-child {
        grid-column: 1 / -1;
      }
      
      .checkbox-container {
        grid-column: 1 / -1;
        padding: 8px;
      }
    }
  `]
})
export class EmployeeDialogComponent {
  employeeForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<EmployeeDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Employee | null
  ) {
    this.employeeForm = this.fb.group({
      documentNumber: [data?.documentNumber || '', Validators.required],
      firstName: [data?.firstName || '', Validators.required],
      lastName: [data?.lastName || '', Validators.required],
      email: [data?.email || '', [Validators.required, Validators.email]],
      phoneNumber: [data?.phoneNumber || '', Validators.required],
      status: [data?.status ?? true]
    });
  }

  onSubmit(): void {
    if (this.employeeForm.valid) {
      this.dialogRef.close(this.employeeForm.value);
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
}
