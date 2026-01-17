import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [CommonModule],   // ✅ REQUIRED for *ngFor, *ngIf
  templateUrl: './user-dashboard.component.html',
})
export class UserDashboardComponent implements OnInit {
  units: any[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:5000/api/user/units')
      .subscribe(data => {
        this.units = data;
      });
  }
}
