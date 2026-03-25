import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { HomeComponent } from './pages/home/home.component';
import { AdminComponent } from './pages/admin/admin.component';
import { authGuard } from './guards/auth.guard';
import { adminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // 🔐 Tenant dashboard (lazy-loaded)
  {
    path: 'tenant-dashboard',
    loadComponent: () =>
      import('./pages/tenant-dashboard/tenant-dashboard.component')
        .then(m => m.TenantDashboardComponent),
    canActivate: [authGuard]
  },

  
  { path: 'admin', component: AdminComponent, canActivate: [adminGuard] },

  { path: '**', redirectTo: 'home' },
];