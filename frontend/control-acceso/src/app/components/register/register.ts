import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { CreateUserRequest, CreateUserResponse } from '../../models/auth.model';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatProgressSpinnerModule,
    MatSnackBarModule
  ],
  templateUrl: './register.html',
  styleUrl: './register.scss'
})
export class Register {
  protected userId = signal<number | null>(null);
  protected password = signal('');
  protected confirmPassword = signal('');
  protected hidePassword = signal(true);
  protected hideConfirmPassword = signal(true);
  protected loading = signal(false);

  private apiUrl = `${environment.apiUrl}${environment.endpoints.login}`;

  constructor(
    private http: HttpClient,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  onSubmit(): void {
    // Validaciones
    if (!this.userId() || !this.password() || !this.confirmPassword()) {
      this.snackBar.open('Todos los campos son obligatorios', 'Cerrar', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
      return;
    }

    if (this.password() !== this.confirmPassword()) {
      this.snackBar.open('Las contraseñas no coinciden', 'Cerrar', {
        duration: 3000,
        panelClass: ['error-snackbar']
      });
      return;
    }

    if (this.password().length < 6) {
      this.snackBar.open('La contraseña debe tener al menos 6 caracteres', 'Cerrar', {
        duration: 3000,
        panelClass: ['warning-snackbar']
      });
      return;
    }

    this.loading.set(true);

    const request: CreateUserRequest = {
      userId: this.userId()!,
      password: this.password()
    };

    this.http.post<CreateUserResponse>(`${this.apiUrl}/login/createuser`, request)
      .subscribe({
        next: (response) => {
          this.loading.set(false);
          
          if (response.success) {
            this.snackBar.open('Usuario registrado exitosamente', 'Cerrar', {
              duration: 3000,
              panelClass: ['success-snackbar']
            });
            
            // Redirigir al login después de 1.5 segundos
            setTimeout(() => {
              this.router.navigate(['/login']);
            }, 1500);
          } else {
            this.snackBar.open(response.message || 'Error al registrar usuario', 'Cerrar', {
              duration: 4000,
              panelClass: ['error-snackbar']
            });
          }
        },
        error: (error) => {
          this.loading.set(false);
          
          let errorMessage = 'Error al registrar usuario';
          
          if (error.status === 400) {
            errorMessage = 'El usuario ya existe o los datos son inválidos';
          } else if (error.status === 0) {
            errorMessage = 'No se pudo conectar con el servidor';
          }
          
          this.snackBar.open(errorMessage, 'Cerrar', {
            duration: 4000,
            panelClass: ['error-snackbar']
          });
        }
      });
  }

  togglePasswordVisibility(): void {
    this.hidePassword.set(!this.hidePassword());
  }

  toggleConfirmPasswordVisibility(): void {
    this.hideConfirmPassword.set(!this.hideConfirmPassword());
  }
}
