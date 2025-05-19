import { HttpEvent, HttpHandler, HttpInterceptor, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { catchError, Observable, switchMap, throwError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);

  const accessToken = localStorage.getItem('access_token');

  const authReq = accessToken
    ? req.clone({
      setHeaders: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
    : req;

  return next(authReq).pipe(
    catchError((error) => {
      if (error.status === 401 && !req.url.includes('/token/refresh/')) {
        return authService.refreshToken().pipe(
          switchMap((response: any) => {
            authService.setTokens(response.access, response.refresh);
            const newReq = req.clone({
              setHeaders: {
                Authorization: `Bearer ${response.access}`,
              },
            });
            return next(newReq);
          }),
          catchError(err => {
            authService.logout();
            return throwError(() => err);
          })
        );
      }
      return throwError(() => error);
    })
  );
};
