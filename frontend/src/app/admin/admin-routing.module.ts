import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AdminDashboardComponent } from './dashboard/admin-dashboard.component';
import { UnitListComponent } from './units/unit-list.component';
import { UnitFormComponent } from './units/unit-form.component';

const routes: Routes = [
  {
    path: '',
    component: AdminDashboardComponent,
    children: [
      // ✅ DEFAULT route (THIS FIXES BLANK PAGE)
      { path: '', redirectTo: 'admin', pathMatch: 'full' },

      { path: '/admin/unitstatus', component: UnitListComponent },
      { path: 'admin/units', component: UnitFormComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule {}
