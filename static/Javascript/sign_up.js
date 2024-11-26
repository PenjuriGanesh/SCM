function validateForm(event) {
    // Prevent form from submitting if validation fails
    event.preventDefault();
    
    clearErrors();
  
    let valid = true;
  
    // Get values from the form fields
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();
    const terms = document.getElementById('terms').checked;
  
    // Validate username
    if (username === '') {
        document.getElementById('usernameError').textContent = 'Username is required.';
        valid = false;
    } else if (username.length < 3 || username.length > 20) {
        document.getElementById('usernameError').textContent = 'Username must be between 3 and 20 characters.';
        valid = false;
    } else if (/[^a-zA-Z0-9]/.test(username)) {
        document.getElementById('usernameError').textContent = 'Username can only contain letters and numbers.';
        valid = false;
    } else if (!/^[A-Z]/.test(username)) { // Username must start with a capital letter
        document.getElementById('usernameError').textContent = 'Username must start with a capital letter.';
        valid = false;
    }
  
    // Validate email
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (email === '') {
        document.getElementById('emailError').textContent = 'Email is required.';
        valid = false;
    } else if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Please enter a valid email address.';
        valid = false;
    } else if (/\s/.test(email)) {  // No spaces allowed in the email
        document.getElementById('emailError').textContent = 'Email cannot contain spaces.';
        valid = false;
    } else if (/^[^a-zA-Z]/.test(email)) { // Email should not start with a number or special character
        document.getElementById('emailError').textContent = 'Email should not start with a number or special character.';
        valid = false;
    }
  
    // Check if email is already registered (no AJAX, using a hardcoded list)
    const existingEmails = ['test@example.com', 'user@domain.com'];  // Simulated list of registered emails
    if (existingEmails.includes(email)) {
        document.getElementById('emailError').textContent = 'This email is already registered.';
        valid = false;
    }
  
    // Validate password
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$/;
    if (password === '') {
        document.getElementById('passwordError').textContent = 'Password is required.';
        valid = false;
    } else if (!passwordRegex.test(password)) {
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters long, start with an uppercase letter, and contain at least one number and one special character.';
        valid = false;
    } else if (!/^[A-Z]/.test(password)) { // Password must start with an uppercase letter
        document.getElementById('passwordError').textContent = 'Password must start with an uppercase letter.';
        valid = false;
    }
  
    // Validate confirm password
    if (confirmPassword === '') {
        document.getElementById('confirmPasswordError').textContent = 'Please confirm your password.';
        valid = false;
    } else if (confirmPassword !== password) {
        document.getElementById('confirmPasswordError').textContent = 'Passwords do not match.';
        valid = false;
    }
  
    // Validate terms checkbox
    if (!terms) {
        alert('You must agree to the Terms & Conditions.');
        valid = false;
    }
  
    // If the form is valid, show success alert and reset the form (simulating a successful signup)
    if (valid) {
        alert('Signup successful! Welcome to our platform.');
        document.getElementById('signupForm').reset(); // Reset the form after successful signup (optional)
    }
}
  
// Clear error messages
function clearErrors() {
    document.getElementById('usernameError').textContent = '';
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    document.getElementById('confirmPasswordError').textContent = '';
}
