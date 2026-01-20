import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-tower-manager',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tower-manager.component.html',
})
export class TowerManagerComponent {
  @Input() towerForm: any = { name: '', floors: 0 };
  @Input() towers: any[] = [];

  @Output() addTowerEvent = new EventEmitter<void>();

  onAddTower() {
    this.addTowerEvent.emit();
  }
}
