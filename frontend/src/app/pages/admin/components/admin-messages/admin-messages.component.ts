import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-admin-messages',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin-messages.component.html',
})
export class AdminMessagesComponent {
  @Input() successMsg = '';
  @Input() errorMsg = '';
}
