import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  loading = false;
  successMsg = '';
  errorMsg = '';
  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    // ✅ Create form here
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      email: ['', [Validators.required, Validators.email]],
      phone: [''],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  submit() {
    this.errorMsg = '';
    this.successMsg = '';
    if (this.form.invalid) return;

    this.loading = true;
    this.auth.register(this.form.value as any).subscribe({
      next: () => {
        this.loading = false;
        this.successMsg = '✅ Registered successfully! Redirecting...';
        setTimeout(() => this.router.navigate(['/login']), 1200);
      },
      error: (err) => {
        this.loading = false;
        this.errorMsg = err?.error?.message || err?.error?.error || 'Register failed';
      },
    });
  }
}
