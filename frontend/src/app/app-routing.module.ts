import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { UserDashboardComponent } from './user/dashboard/user-dashboard.component';
import { AdminDashboardComponent } from './admin/dashboard/admin-dashboard.component';
import { AdminGuard } from './core/guards/admin.guard';


const routes: Routes = [
{ path: '', component: LoginComponent },
{ path: 'register', component: RegisterComponent },
{ path: 'user', component: UserDashboardComponent },
{ path: 'admin', component: AdminDashboardComponent, canActivate: [AdminGuard] }
];


@NgModule({ imports: [RouterModule.forRoot(routes)], exports: [RouterModule] })
export class AppRoutingModule {}