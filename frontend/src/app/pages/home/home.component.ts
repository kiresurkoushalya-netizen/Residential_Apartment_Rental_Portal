import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit {
  baseUrl = 'http://localhost:5000/api';

  units: any[] = [];
  loading = false;
  errorMsg = '';
  successMsg = '';

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef   // ✅ ADD THIS
  ) {}

  ngOnInit(): void {
    this.loadUnits();
  }

  loadUnits() {
    this.loading = true;
    this.errorMsg = '';
    this.cdr.detectChanges(); // ✅ refresh UI immediately

    this.http.get<any[]>(`${this.baseUrl}/units?status=available`).subscribe({
      next: (res) => {
        const data = Array.isArray(res) ? res : [];

        // ✅ assign fresh array
        this.units = [...data];

        this.loading = false;

        // ✅ force UI update
        this.cdr.detectChanges();

        console.log("✅ Units assigned:", this.units);
      },
      error: (err) => {
        console.error(err);
        this.loading = false;
        this.errorMsg = 'Failed to load units';

        // ✅ force UI update
        this.cdr.detectChanges();
      }
    });
  }

  getUnitImage(index: number): string {
    const images = [
      'assets/units/flat1.jpg',
      'assets/units/flat2.jpg',
      'assets/units/flat3.jpg',
      'assets/units/flat4.jpg',
      'assets/units/flat5.jpg'
    ];

    return images[index % images.length];
  }

 requestBooking(unitId: number) {
  this.successMsg = '';
  this.errorMsg = '';

  const token = localStorage.getItem('token');
  if (!token) {
    this.errorMsg = 'Login required to request booking';
    this.router.navigate(['/login']);
    return;
  }

  const payload = {
    unit_id: unitId,
    visit_date: new Date().toISOString().slice(0, 10), // ✅ REQUIRED
    notes: 'Requested from home'
  };

  console.log("✅ Booking payload:", payload);

  this.http.post(
    `${this.baseUrl}/bookings`,
    payload, // ✅ IMPORTANT: send payload object here
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }
  ).subscribe({
    next: () => {
      this.successMsg = '✅ Booking request sent successfully';
    },
    error: (err) => {
      console.error(err);
      this.errorMsg = err?.error?.error || 'Booking request failed';
    }
  });
}



  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
