import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class AdminService {

  private baseUrl = 'http://localhost:5000/api/admin';

  constructor(private http: HttpClient) {}

  // -----------------------------
  // Towers
  // -----------------------------

  addTower(data: { name: string; location: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/towers`, data);
  }

  getTowers(): Observable<any> {
    return this.http.get(`${this.baseUrl}/towers`);
  }

  // -----------------------------
  // Units
  // -----------------------------

  addUnit(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/units`, data);
  }

  getUnits(): Observable<any> {
    return this.http.get(`${this.baseUrl}/units`);
  }

  deleteUnit(unitId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/units/${unitId}`);
  }

  // -----------------------------
  // Bookings
  // -----------------------------

  approveBooking(id: number): Observable<any> {
    return this.http.put(`${this.baseUrl}/bookings/${id}/approve`, {});
  }

  declineBooking(id: number, reason: string): Observable<any> {
    return this.http.put(`${this.baseUrl}/bookings/${id}/decline`, { reason });
  }

}