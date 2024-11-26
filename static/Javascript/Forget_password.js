function validateForm(event) {
    // Prevent form from submitting if validation fails
    event.preventDefault();
    
    clearErrors();
  
    let valid = true;
  
    // Get the email value
    const email = document.getElementById('email').value.trim();
  
    // Validate email
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (email === '') {
        document.getElementById('emailError').textContent = 'Email is required.';
        valid = false;
    } else if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Please enter a valid email address (e.g. user@example.com).';
        valid = false;
    } else if (/\s/.test(email)) {  // No spaces allowed in the email
        document.getElementById('emailError').textContent = 'Email cannot contain spaces.';
        valid = false;
    }
  
    // Check if email is already registered (no AJAX, using a hardcoded list)
    const existingEmails = ['test@example.com', 'user@domain.com'];  // Simulated list of registered emails
    if (!existingEmails.includes(email)) {
        document.getElementById('emailError').textContent = 'This email is not registered.';
        valid = false;
    }
  
    // If the form is valid, show success alert and reset the form (simulating a successful password reset request)
    if (valid) {
        alert('Password reset request sent! Check your email for further instructions.');
        document.getElementById('forgotPasswordForm').reset(); // Reset the form after successful request
    }
}

// Clear error messages
function clearErrors() {
    document.getElementById('emailError').textContent = '';
}
