import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { AuthService } from '../../services/auth.service';
import { AuthRequest } from '../../models/auth.model';

@Component({
  selector: 'app-login',
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
  templateUrl: './login.html',
  styleUrl: './login.scss'
})
export class Login {
  userId: number | null = null;
  password: string = '';
  hidePassword = signal(true);
  loading = signal(false);
  attemptCount = signal(0);
  maxAttempts = 3;
  private returnUrl: string = '/dashboard';

  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar
  ) {
    // Obtener URL de retorno si existe
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
  }

  onSubmit(): void {
    if (!this.userId || !this.password) {
      this.showMessage('Por favor ingrese usuario y contraseña', 'error');
      return;
    }

    this.loading.set(true);

    const request: AuthRequest = {
      userId: this.userId,
      password: this.password
    };

    this.authService.login(request).subscribe({
      next: (response) => {
        this.loading.set(false);
        
        if (response.success && response.token) {
          this.showMessage('¡Login exitoso! Bienvenido', 'success');
          this.attemptCount.set(0);
          
          // Redirigir después de un breve delay
          setTimeout(() => {
            this.router.navigate([this.returnUrl]);
          }, 500);
        } else if (response.locked) {
          this.showMessage(response.message, 'error', 5000);
          this.password = '';
        } else {
          this.attemptCount.update(count => count + 1);
          const remainingAttempts = this.maxAttempts - this.attemptCount();
          
          if (remainingAttempts > 0) {
            this.showMessage(
              `${response.message}. Intentos restantes: ${remainingAttempts}`, 
              'warning', 
              4000
            );
          }
          
          this.password = '';
        }
      },
      error: (err) => {
        this.loading.set(false);
        this.password = '';
        
        if (err.status === 423) {
          // Cuenta bloqueada
          this.showMessage(
            'Cuenta bloqueada por múltiples intentos fallidos. Intente en 10 minutos.', 
            'error', 
            6000
          );
        } else if (err.status === 401) {
          // Credenciales inválidas
          this.attemptCount.update(count => count + 1);
          const remainingAttempts = this.maxAttempts - this.attemptCount();
          
          if (remainingAttempts > 0) {
            this.showMessage(
              `Credenciales inválidas. Intentos restantes: ${remainingAttempts}`, 
              'warning', 
              4000
            );
          } else {
            this.showMessage(
              'Cuenta bloqueada por múltiples intentos fallidos.', 
              'error', 
              5000
            );
          }
        } else {
          this.showMessage('Error de conexión. Intente nuevamente.', 'error');
        }
        
        console.error('Error en login:', err);
      }
    });
  }

  togglePasswordVisibility(): void {
    this.hidePassword.update(value => !value);
  }

  private showMessage(message: string, type: 'success' | 'error' | 'warning', duration: number = 3000): void {
    this.snackBar.open(message, 'Cerrar', {
      duration,
      horizontalPosition: 'center',
      verticalPosition: 'top',
      panelClass: `${type}-snackbar`
    });
  }
}
