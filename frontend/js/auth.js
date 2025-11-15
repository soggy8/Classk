// Authentication JavaScript

document.addEventListener('DOMContentLoaded', function () {
  const loginForm = document.getElementById('loginForm');
  const signupForm = document.getElementById('signupForm');

  // Show / hide password for any .toggle-password button
  const toggleButtons = document.querySelectorAll('.toggle-password');

  toggleButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const wrapper = btn.closest('.input-wrapper');
      if (!wrapper) return;

      const input = wrapper.querySelector('input[type="password"], input[type="text"]');
      if (!input) return;

      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';
      btn.textContent = isPassword ? 'Hide' : 'Show';
    });
  });

  // Login form validation
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      const emailEl = document.getElementById('email');
      const passwordEl = document.getElementById('password');

      const email = emailEl ? emailEl.value.trim() : '';
      const password = passwordEl ? passwordEl.value : '';

      if (!email || !password) {
        e.preventDefault();
        alert('Please enter both email and password.');
        return false;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        e.preventDefault();
        alert('Please enter a valid email address.');
        return false;
      }
    });
  }

  // Signup form validation
  if (signupForm) {
    signupForm.addEventListener('submit', function (e) {
      const nameEl = document.getElementById('name');
      const emailEl = document.getElementById('email');
      const passwordEl = document.getElementById('password');
      const majorGroupEl = document.getElementById('major_group');

      const name = nameEl ? nameEl.value.trim() : '';
      const email = emailEl ? emailEl.value.trim() : '';
      const password = passwordEl ? passwordEl.value : '';
      const majorGroup = majorGroupEl ? majorGroupEl.value.trim() : '';

      if (!name || !email || !password || !majorGroup) {
        e.preventDefault();
        alert('Please fill in all fields.');
        return false;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        e.preventDefault();
        alert('Please enter a valid email address.');
        return false;
      }

      if (password.length < 6) {
        e.preventDefault();
        alert('Password must be at least 6 characters long.');
        return false;
      }
    });
  }
});
