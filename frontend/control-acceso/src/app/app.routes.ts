import { Routes } from '@angular/router';
import { Dashboard } from './components/dashboard/dashboard';
import { Empleados } from './components/empleados/empleados';
import { ControlAcceso } from './components/control-acceso/control-acceso';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: Dashboard, title: 'Dashboard - Control de Acceso' },
  { path: 'empleados', component: Empleados, title: 'Gestión de Empleados' },
  { path: 'acceso', component: ControlAcceso, title: 'Control de Acceso' },
  { path: '**', redirectTo: '/dashboard' }
];
