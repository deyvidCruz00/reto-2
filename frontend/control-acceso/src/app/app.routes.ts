import { Routes } from '@angular/router';
import { Dashboard } from './components/dashboard/dashboard';
import { Empleados } from './components/empleados/empleados';
import { ControlAcceso } from './components/control-acceso/control-acceso';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: Login, title: 'Login - Control de Acceso' },
  { path: 'register', component: Register, title: 'Registro - Control de Acceso' },
  { 
    path: '', 
    canActivate: [AuthGuard],
    children: [
      { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: Dashboard, title: 'Dashboard - Control de Acceso' },
      { path: 'empleados', component: Empleados, title: 'Gestión de Empleados' },
      { path: 'acceso', component: ControlAcceso, title: 'Control de Acceso' },
    ]
  },
  { path: '**', redirectTo: '/login' }
];
