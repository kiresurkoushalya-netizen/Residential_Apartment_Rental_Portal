import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-unit-manager',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './unit-manager.component.html',
})
export class UnitManagerComponent {
  @Input() unitForm: any = {};
  @Input() towers: any[] = [];
  @Input() units: any[] = [];

  @Output() addUnitEvent = new EventEmitter<void>();
  @Output() deleteUnitEvent = new EventEmitter<number>();

  onAddUnit() {
    this.addUnitEvent.emit();
  }

  onDelete(id: number) {
    this.deleteUnitEvent.emit(id);
  }
}
