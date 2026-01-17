import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class UnitService {
  private adminAPI = 'http://localhost:5000/api/admin';

  private API = 'http://localhost:5000/api/admin/units';
 

  constructor(private http: HttpClient) {}

  addUnit(data: any) {
  return this.http.post(
    `${this.adminAPI}/units`,
    data,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    }
  );
}  
 
getAllUnits(): Observable<any> {
    const token = localStorage.getItem('token');

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.get(this.API, { headers });
  }

}
