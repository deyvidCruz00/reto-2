import { Component, signal, computed } from '@angular/core';
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
  
  // Authentication state
  protected readonly isAuthenticated = computed(() => this.authService.isAuthenticated());
  protected readonly userId = computed(() => this.authService.getUserId());
  
  menuItems = [
    { path: '/dashboard', icon: 'dashboard', label: 'Dashboard' },
    { path: '/empleados', icon: 'people', label: 'Empleados' },
    { path: '/acceso', icon: 'door_sliding', label: 'Control de Acceso' }
  ];
  
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}
  
  toggleSidenav(): void {
    this.sidenavOpened.set(!this.sidenavOpened());
  }
  
  logout(): void {
    this.authService.logout();
  }
}
