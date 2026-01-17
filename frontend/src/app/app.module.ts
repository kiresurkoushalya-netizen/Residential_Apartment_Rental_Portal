import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { UserDashboardComponent } from './user/dashboard/user-dashboard.component';
import { AdminDashboardComponent } from './admin/dashboard/admin-dashboard.component';

export const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // 🔥 ADD THESE
  { path: 'user', component: UserDashboardComponent },
  { path: 'admin', component: AdminDashboardComponent },

  // fallback
  { path: '**', redirectTo: '' }
];
