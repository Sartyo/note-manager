import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  signupForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService) {
    this.signupForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.signupForm.valid) {
      const { username, password } = this.signupForm.value;
      console.log('Registration attempt:', username, password);
      if (username && password) {
        this.authService.signup(username, password).subscribe({
          next: () => alert('Signup successful. Please login.'),
          error: () => alert('Signup failed.')
        });
      }
    }
  }
}
