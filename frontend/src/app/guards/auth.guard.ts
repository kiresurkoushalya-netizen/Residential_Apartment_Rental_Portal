import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { AuthService } from '../service/auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const token = localStorage.getItem('access_token');

  // ✅ DIRECT token check (no timing issue)
  if (token) {
    return true;
  }

  // ❌ No token → redirect once
  router.navigate(['/login']);
  return false;
};