import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UnitService {

  private API = 'http://localhost:5000/api';

  // 🔥 SINGLE SOURCE OF TRUTH
  private unitsSubject = new BehaviorSubject<any[]>([]);
  units$ = this.unitsSubject.asObservable();

  constructor(private http: HttpClient) {}

  // ----------------------------------
  // TENANT / PUBLIC
  // ----------------------------------

  /** ✅ Load AVAILABLE units ONCE and persist */
  loadAvailableUnits(): Observable<any[]> {
    console.log('Calling API: /units?status=available');

    return this.http
      .get<any[]>(`${this.API}/units?status=available`)
      .pipe(
        tap(units => {
          console.log('Persisting units in service:', units);
          this.unitsSubject.next(units);
        })
      );
  }

  /** ✅ Snapshot (no API, no flicker) */
  getUnitsSnapshot(): any[] {
    return this.unitsSubject.value;
  }

  /** ✅ Remove unit after booking */
  removeUnit(unitId: number): void {
    const updated = this.unitsSubject.value.filter(
      unit => unit.id !== unitId
    );
    this.unitsSubject.next(updated);
  }

  /** ✅ Booking API */
  requestBooking(
    unitId: number,
    visitDate: string,
    notes?: string
  ): Observable<any> {
    return this.http.post(`${this.API}/bookings`, {
      unit_id: unitId,
      visit_date: visitDate,
      notes
    });
  }
}