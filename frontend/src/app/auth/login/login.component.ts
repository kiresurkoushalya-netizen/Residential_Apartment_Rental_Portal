import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  loading = false;
  errorMsg = '';
  form!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    // ✅ Initialize inside constructor
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(4)]],
    });
  }

  submit() {
  this.errorMsg = '';

  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }

  this.loading = true;

  this.auth.login(this.form.value).subscribe({
    next: (res) => {
      this.loading = false;

      // ✅ 1. STORE TOKEN (VERY IMPORTANT)
      localStorage.setItem('access_token', res.access_token);

      // ✅ 2. (OPTIONAL) STORE USER INFO
      localStorage.setItem('user', JSON.stringify(res.user));

      // ✅ 3. ROLE-BASED NAVIGATION
      if (res.role === 'admin') {
        this.router.navigate(['/admin']);
      } else {
        this.router.navigate(['/tenant-dashboard']);
      }
    },
    error: () => {
      this.loading = false;
      this.errorMsg = 'Invalid credentials';
    }
  });
  }
}
