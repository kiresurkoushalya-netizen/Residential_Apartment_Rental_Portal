import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-admin-header',
  standalone: true,
  templateUrl: './admin-header.component.html',
})
export class AdminHeaderComponent {
  @Output() logoutEvent = new EventEmitter<void>();

  onLogout() {
    this.logoutEvent.emit();
  }
}
