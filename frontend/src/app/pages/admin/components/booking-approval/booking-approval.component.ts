import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-booking-approval',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './booking-approval.component.html',
})
export class BookingApprovalComponent {
  @Input() bookings: any[] = [];
  @Input() loading = false;
  @Input() bookingStatusFilter = 'pending';
  @Input() declineReason: { [key: number]: string } = {};

  @Output() filterChanged = new EventEmitter<string>();
  @Output() approveEvent = new EventEmitter<number>();
  @Output() declineEvent = new EventEmitter<number>();

  onFilterChange() {
    this.filterChanged.emit(this.bookingStatusFilter);
  }

  approve(id: number) {
    this.approveEvent.emit(id);
  }

  decline(id: number) {
    this.declineEvent.emit(id);
  }
}
