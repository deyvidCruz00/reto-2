import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatMenuModule } from '@angular/material/menu';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('Sistema de Control de Acceso');
  sidenavOpened = signal(true);
  
  // Authentication state - usando el observable del servicio
  protected readonly isAuthenticated = signal(false);
  protected readonly userId = signal<number | null>(null);
  
  menuItems = [
    { path: '/dashboard', icon: 'dashboard', label: 'Dashboard' },
    { path: '/empleados', icon: 'people', label: 'Empleados' },
    { path: '/acceso', icon: 'door_sliding', label: 'Control de Acceso' }
  ];
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    // Suscribirse al estado de autenticación
    this.authService.isAuthenticated$.subscribe(isAuth => {
      this.isAuthenticated.set(isAuth);
      if (isAuth) {
        this.userId.set(this.authService.getUserId());
      } else {
        this.userId.set(null);
      }
    });
  }
  
  toggleSidenav(): void {
    this.sidenavOpened.set(!this.sidenavOpened());
  }
  
  logout(): void {
    this.authService.logout();
  }
}
