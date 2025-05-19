import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, tap } from 'rxjs';
import { getTokenExpiration } from './token-utils';

interface LoginResponse {
  access: string;
  refresh: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://localhost:8000/auth';
  private loggedIn$ = new BehaviorSubject<boolean>(this.hasToken());
  private refreshTimer: any;

  constructor(private http: HttpClient, private router: Router) { }

  login(username: string, password: string) {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login/`, { username, password }).pipe(
      tap((res) => {
        localStorage.setItem('access_token', res.access);
        localStorage.setItem('refresh_token', res.refresh);
        this.loggedIn$.next(true);
        this.router.navigate(['/notes']);
      })
    );
  }

  signup(username: string, password: string) {
    return this.http.post(`${this.baseUrl}/signup`, { username, password });
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    clearTimeout(this.refreshTimer);
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  private hasToken(): boolean {
    return !!localStorage.getItem('access_token');
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  refreshToken() {
    const refresh = localStorage.getItem('refresh_token');
    return this.http.post<any>('http://localhost:8000/auth/token/refresh/', {
      refresh
    });
  }

  setTokens(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    this.scheduleRefresh(access);
  }

  private scheduleRefresh(accessToken: string) {
    clearTimeout(this.refreshTimer);

    const exp = getTokenExpiration(accessToken);
    if (!exp) return;

    const delay = exp - Date.now() - 10000;

    if (delay > 0) {
      this.refreshTimer = setTimeout(() => {
        this.refreshToken().subscribe({
          next: (tokens) => this.setTokens(tokens.access, tokens.refresh),
          error: () => this.logout()
        });
      }, delay);
    }
  }

  initialize() {
    const token = localStorage.getItem('access_token');
    if (token) {
      this.scheduleRefresh(token);
    }
  }
}
