import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { UnitService } from '../services/unit.service';

@Component({
  selector: 'app-unit-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './unit-form.component.html'
})
export class UnitFormComponent {
  unitForm: FormGroup;
  submitted = false;

  successMessage = '';
  errorMessage = '';

  constructor(private fb: FormBuilder, private unitService: UnitService) {
    this.unitForm = this.fb.group({
      tower: ['', Validators.required],
      unitNumber: ['', Validators.required],
      floor: [1],
      rent: [1000, [Validators.required, Validators.min(1000)]],
      status: ['available']
    });
  }

  submit() {
    this.submitted = true;

    if (this.unitForm.invalid) {
      return;
    }

    this.unitService.addUnit(this.unitForm.value).subscribe({
      next: () => {
        this.successMessage = 'Unit added successfully';
        this.errorMessage = '';
        this.unitForm.reset();
        this.submitted = false;
      },
      error: () => {
        this.errorMessage = 'Failed to add unit';
        this.successMessage = '';
      }
    });
  }
}
