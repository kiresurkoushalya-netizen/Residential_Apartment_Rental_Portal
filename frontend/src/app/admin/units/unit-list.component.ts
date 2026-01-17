import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UnitService } from '../services/unit.service';

@Component({
  selector: 'app-unit-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './unit-list.component.html'
})
export class UnitListComponent implements OnInit {

  units: any[] = [];

  constructor(private unitService: UnitService) {}

  ngOnInit(): void {
    console.log("✅ UnitListComponent Loaded");
    this.loadUnits();
  }

  loadUnits(): void {
    console.log("✅ Calling API /api/admin/units");

    this.unitService.getAllUnits().subscribe({
      next: (res: any) => {
        console.log("✅ API Response:", res);
        this.units = res?.units || [];
        console.log("✅ Units assigned:", this.units);
      },
      error: (err: any) => {
        console.error("❌ API Error:", err);
      }
    });
  }
}
