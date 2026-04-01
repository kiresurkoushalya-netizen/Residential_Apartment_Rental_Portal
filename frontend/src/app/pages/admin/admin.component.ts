import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.component.html',
})
export class AdminComponent implements OnInit {
  baseUrl = 'http://localhost:5000/api';

  // Common UI
  loading = false;
  errorMsg = '';
  successMsg = '';

  // Dashboard
  occupancy: any = null;

  // Bookings
  bookings: any[] = [];
  bookingStatusFilter: string = 'pending';
  declineReason: { [key: number]: string } = {};

  // Towers
  towers: any[] = [];
  towerForm = {
    name: '',
    floors: ''
  };

  // Amenities
  amenities: any[] = [];

  // ✅ IMPORTANT (selected amenities)
  selectedAmenities: number[] = [];

  // Units
  units: any[] = [];
  unitForm = {
    tower_id: '',
    unit_no: '',
    floor: '',
    bhk: '2BHK',
    rent: '',
    status: 'available',
    furnishing_type: ''
  };

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
    this.loadTowers();
    this.loadUnits();
    this.loadBookings();
    this.getAmenities();
  }

  // -------------------------
  // Helpers
  // -------------------------
  clearMsgs() {
    this.errorMsg = '';
    this.successMsg = '';
  }

  private authOptions() {
    const token = localStorage.getItem('token');

    if (!token) {
      this.errorMsg = 'Token missing. Please login again.';
      this.router.navigate(['/login']);
      return null;
    }

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      }),
    };
  }

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }

  // -------------------------
  // Dashboard
  // -------------------------
  loadDashboard() {
    const opts = this.authOptions();
    if (!opts) return;

    this.http.get(`${this.baseUrl}/admin/dashboard/occupancy`, opts).subscribe({
      next: (res) => {
        this.occupancy = res;
      },
      error: () => {
        this.errorMsg = "Failed to load dashboard";
      },
    });
  }

  // -------------------------
  // Towers
  // -------------------------
  loadTowers() {
    this.http.get<any[]>(`${this.baseUrl}/tower/towers`).subscribe({
      next: (res) => {
        this.towers = res || [];
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMsg = 'Failed to load towers';
      },
    });
  }

  addTower() {
    this.clearMsgs();

    if (!this.towerForm.name || !this.towerForm.floors) {
      this.errorMsg = 'Tower name and floors required';
      return;
    }

    const payload = {
      name: this.towerForm.name,
      floors: Number(this.towerForm.floors),
    };

    const opts = this.authOptions();
    if (!opts) return;

    this.http.post(`${this.baseUrl}/tower/admin/towers`, payload, opts).subscribe({
      next: () => {
        this.successMsg = '✅ Tower added';
        this.towerForm = { name: '', floors: '' };
        this.loadTowers();
      },
      error: (err) => {
        this.errorMsg = err?.error?.error || 'Failed to add tower';
      },
    });
  }

  // -------------------------
  // Units
  // -------------------------
  loadUnits() {
    const opts = this.authOptions();
    if (!opts) return;

    this.http.get<any>(`${this.baseUrl}/admin/units`, opts).subscribe({
      next: (res) => {
        this.units = res?.units || [];
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMsg = 'Failed to load units';
      },
    });
  }

  getAmenities() {
    this.http.get<any[]>(`${this.baseUrl}/amenities`)
      .subscribe({
        next: (data) => {
          console.log("🔥 Amenities API:", data);
          this.amenities = data;
        },
        error: (err) => {
          console.error("❌ Amenities error:", err);
        }
      });
  }

  // ✅ FIXED FUNCTION
  onAmenityChange(event: any) {
    const id = Number(event.target.value);

    if (event.target.checked) {
      this.selectedAmenities.push(id);
    } else {
      this.selectedAmenities = this.selectedAmenities.filter(a => a !== id);
    }

    console.log("Selected Amenities:", this.selectedAmenities);
  }

  showAmenityDropdown = false;

  toggleAmenityDropdown() {
    this.showAmenityDropdown = !this.showAmenityDropdown;
  }

  // ✅ FINAL FIXED ADD UNIT
  addUnit() {
    this.clearMsgs();

    if (
      !this.unitForm.tower_id ||
      !this.unitForm.unit_no ||
      !this.unitForm.floor ||
      !this.unitForm.bhk ||
      !this.unitForm.rent
    ) {
      this.errorMsg = 'Fill all unit fields';
      return;
    }

    const payload = {
      tower_id: Number(this.unitForm.tower_id),
      unit_no: this.unitForm.unit_no,
      floor: Number(this.unitForm.floor),
      bhk: this.unitForm.bhk,
      rent: Number(this.unitForm.rent),
      status: this.unitForm.status,
      furnishing_type: this.unitForm.furnishing_type,

      // ✅ CRITICAL FIX
      amenity_ids : this.selectedAmenities
    };

    const opts = this.authOptions();
    if (!opts) return;

    this.http.post(`${this.baseUrl}/admin/units`, payload, opts).subscribe({
      next: () => {
        this.successMsg = '✅ Unit added';

        // ✅ RESET FORM
        this.unitForm = {
          tower_id: '',
          unit_no: '',
          floor: '',
          bhk: '2BHK',
          rent: '',
          status: 'available',
          furnishing_type: ''
        };

        // ✅ RESET AMENITIES
        this.selectedAmenities = [];

        this.loadUnits();
      },
      error: (err) => {
        this.errorMsg = err?.error?.error || 'Failed to add unit';
      },
    });
  }

  deleteUnit(id: number) {
    this.clearMsgs();

    if (!confirm('Are you sure you want to delete this unit?')) return;

    const opts = this.authOptions();
    if (!opts) return;

    this.http.delete(`${this.baseUrl}/admin/units/${id}`, opts).subscribe({
      next: () => {
        this.successMsg = '✅ Unit deleted';
        this.loadUnits();
      },
      error: () => {
        this.errorMsg = 'Delete failed';
      },
    });
  }

  // -------------------------
  // Bookings
  // -------------------------
  loadBookings() {
    this.clearMsgs();

    const opts = this.authOptions();
    if (!opts) return;

    this.loading = true;

    this.http
      .get<any[]>(
        `${this.baseUrl}/admin/bookings?status=${this.bookingStatusFilter}`,
        opts
      )
      .subscribe({
        next: (res) => {
          this.bookings = res || [];
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error(err);
          this.loading = false;
          this.errorMsg = 'Failed to load bookings';
        },
      });
  }

  approveBooking(id: number) {
    this.clearMsgs();

    const opts = this.authOptions();
    if (!opts) return;

    this.http.put(`${this.baseUrl}/admin/bookings/${id}/approve`, {}, opts).subscribe({
      next: () => {
        this.successMsg = '✅ Booking approved';
        this.loadBookings();
      },
      error: () => {
        this.errorMsg = 'Approve failed';
      },
    });
  }

  declineBooking(id: number) {
    this.clearMsgs();

    const opts = this.authOptions();
    if (!opts) return;

    const reason = this.declineReason[id] || 'Declined by admin';

    this.http
      .put(`${this.baseUrl}/admin/bookings/${id}/reject`, { reason }, opts)
      .subscribe({
        next: () => {
          this.successMsg = '❌ Booking declined';
          this.loadBookings();
        },
        error: () => {
          this.errorMsg = 'Decline failed';
        },
      });
  }
}