function validateForm(event) {
    // Prevent form from submitting if validation fails
    event.preventDefault();
    
    // Clear any previous error messages
    clearErrors();
  
    let valid = true;
  
    // Get values from the form fields
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const confirmPassword = document.getElementById('confirm-password').value.trim();
    const terms = document.getElementById('terms').checked;
  
    // Username validation (already done in backend, skip this check in JS)
    if (username === '') {
        document.getElementById('usernameError').textContent = 'Username is required.';
        valid = false;
    } else if (username.length < 3 || username.length > 20) {
        document.getElementById('usernameError').textContent = 'Username must be between 3 and 20 characters.';
        valid = false;
    }

    // Email validation (already done in backend, skip this check in JS)
    if (email === '') {
        document.getElementById('emailError').textContent = 'Email is required.';
        valid = false;
    }

    // Password validation
if (password === '') {
    document.getElementById('passwordError').textContent = 'Password is required.';
    valid = false;
}  else if (!/^[A-Z]/.test(password)) {  // Check if password starts with a capital letter
    document.getElementById('passwordError').textContent = 'Password must start with a capital letter.';
    valid = false;
} else if (!/\d/.test(password)) {  // Check if password contains at least one digit
    document.getElementById('passwordError').textContent = 'Password should contain at least one digit.';
    valid = false;
} else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {  // Check if password contains at least one special character
    document.getElementById('passwordError').textContent = 'Password should contain at least one special character.';
    valid = false;
} else if (!/[a-z]/.test(password)) { // Ensure that the password has at least one lowercase letter
    document.getElementById('passwordError').textContent = 'Password should contain at least one lowercase letter.';
    valid = false;
}else if (password.length < 7) {  // Check if password is at least 7 characters long
    document.getElementById('passwordError').textContent = 'Password should be at least 7 characters long.';
    valid = false;
}


    // Confirm password validation
    if (confirmPassword === '') {
        document.getElementById('confirmPasswordError').textContent = 'Please confirm your password.';
        valid = false;
    } else if (confirmPassword !== password) {
        document.getElementById('confirmPasswordError').textContent = 'Passwords do not match.';
        valid = false;
    }

    // Validate terms checkbox
    if (!terms) {
        document.getElementById('termsError').textContent = 'You must agree to the Terms & Conditions.';
        valid = false;
    }
  
    // If the form is valid, show success alert and reset the form (simulating a successful signup)
    if (valid) {
        document.getElementById('signupForm').reset(); // Reset the form after successful signup (optional)
    }
}

// Clear error messages
function clearErrors() {
    document.getElementById('usernameError').textContent = '';
    document.getElementById('emailError').textContent = '';
    document.getElementById('passwordError').textContent = '';
    document.getElementById('confirmPasswordError').textContent = '';
    document.getElementById('termsError').textContent = ''; // Error for terms & conditions
}
