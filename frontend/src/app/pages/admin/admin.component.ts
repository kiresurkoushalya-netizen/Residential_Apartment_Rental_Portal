import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AdminHeaderComponent } from './components/admin-header/admin-header.component';
import { AdminMessagesComponent } from './components/admin-messages/admin-messages.component';
import { AdminSummaryComponent } from './components/admin-summary/admin-summary.component';
import { TowerManagerComponent } from './components/tower-manager/tower-manager.component';
import { UnitManagerComponent } from './components/unit-manager/unit-manager.component';
import { BookingApprovalComponent } from './components/booking-approval/booking-approval.component';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    AdminHeaderComponent,
    AdminMessagesComponent,
    AdminSummaryComponent,
    TowerManagerComponent,
    UnitManagerComponent,
    BookingApprovalComponent
  ],
  templateUrl: './admin.component.html',
})
export class AdminComponent {
  // ✅ your existing variables remain
  successMsg = '';
  errorMsg = '';
  loading = false;

  occupancy: any = null;

  towers: any[] = [];
  units: any[] = [];
  bookings: any[] = [];

  towerForm = { name: '', floors: 0 };
  unitForm = {
    tower_id: '',
    unit_no: '',
    floor: 0,
    bhk: '1BHK',
    rent: 0,
    status: 'available',
  };

  bookingStatusFilter = 'pending';
  declineReason: { [key: number]: string } = {};

  // ✅ your existing functions remain
  logout() {}
  addTower() {}
  addUnit() {}
  deleteUnit(id: number) {}
  loadBookings() {}
  approveBooking(id: number) {}
  declineBooking(id: number) {}

  // ✅ new helper for standalone booking filter change
  onBookingFilterChange(status: string) {
    this.bookingStatusFilter = status;
    this.loadBookings();
  }
}
