import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookingService {

  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // -----------------------------
  // Tenant APIs
  // -----------------------------
  createBooking(data: {
    unit_id: number;
    visit_date: string;
    notes?: string;
  }): Observable<any> {
    return this.http.post(`${this.baseUrl}/bookings`, data);
  }

  requestBooking(unitId: number, visitDate: string, notes: string) {
    return this.http.post(`${this.baseUrl}/bookings`, {
      unit_id: unitId,
      visit_date: visitDate,
      notes
    });
  }


  myBookings(): Observable<any> {
    return this.http.get(`${this.baseUrl}/bookings/my`)
  }

  // -----------------------------
  // Admin APIs
  // -----------------------------
  getAllBookings(status?: string): Observable<any> {
    const URL = status
      ? `${this.baseUrl}/admin/bookings?status=${status}`
      : `${this.baseUrl}/admin/bookings`;

    return this.http.get(URL);
  }
}