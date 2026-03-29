import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { UnitService } from '../../service/unit.service';
import { BookingService } from '../../service/booking.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-tenant-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tenant-dashboard.component.html',
  styleUrls: ['./tenant-dashboard.component.css']
})
export class TenantDashboardComponent implements OnInit {

  // 🔥 SINGLE SOURCE OF TRUTH
  units$!: Observable<any[]>;
  message = '';

  constructor(
    private unitService: UnitService,
    private bookingService: BookingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    console.log('Tenant dashboard loaded');

    // ✅ Bind observable ONCE
    this.units$ = this.unitService.units$;

    // ✅ Load only if empty
    if (this.unitService.getUnitsSnapshot().length === 0) {
      this.unitService.loadAvailableUnits().subscribe();
    }
  }

  

    

  bookUnit(unitId: number) {

  this.message = "⏳ Sending booking request...";

  this.bookingService.requestBooking(
    unitId,
    new Date().toISOString().split('T')[0],
    "Interested"
  ).subscribe({

    next: () => {
      this.message = "✅ Booking requested successfully";

      this.unitService.removeUnit(unitId);
    },

    error: (err) => {
      console.error(err);
      this.message = "❌ Booking failed";
    }

  });

}

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}