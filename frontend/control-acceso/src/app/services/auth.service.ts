import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { AuthRequest, AuthResponse } from '../models/auth.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}${environment.endpoints.login}`;
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(this.hasToken());
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  /**
   * Autentica un usuario en el sistema
   */
  login(request: AuthRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login/authuser`, request).pipe(
      tap(response => {
        if (response.success && response.token) {
          this.setToken(response.token);
          this.setUserId(response.userId);
          this.isAuthenticatedSubject.next(true);
        }
      })
    );
  }

  /**
   * Cierra la sesión del usuario
   */
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    this.isAuthenticatedSubject.next(false);
    this.router.navigate(['/login']);
  }

  /**
   * Verifica si el usuario está autenticado
   */
  isAuthenticated(): boolean {
    return this.hasToken();
  }

  /**
   * Obtiene el token JWT del localStorage
   */
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  /**
   * Obtiene el ID del usuario autenticado
   */
  getUserId(): number | null {
    const userId = localStorage.getItem('userId');
    return userId ? parseInt(userId, 10) : null;
  }

  /**
   * Guarda el token en localStorage
   */
  private setToken(token: string): void {
    localStorage.setItem('token', token);
  }

  /**
   * Guarda el ID del usuario en localStorage
   */
  private setUserId(userId: number): void {
    localStorage.setItem('userId', userId.toString());
  }

  /**
   * Verifica si existe un token
   */
  private hasToken(): boolean {
    return !!localStorage.getItem('token');
  }

  /**
   * Verifica la validez del token (básica, solo verifica expiración)
   */
  isTokenValid(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const expiration = payload.exp * 1000; // Convertir a milisegundos
      return Date.now() < expiration;
    } catch (error) {
      return false;
    }
  }
}
