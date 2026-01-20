import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-summary.component.html',
})
export class AdminSummaryComponent {
  @Input() occupancy: any = null;
}
