 let captchaCode = '';

 // Function to generate a random CAPTCHA code
 function generateCaptcha() {
   const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   let code = '';
   for (let i = 0; i < 6; i++) {
     code += chars.charAt(Math.floor(Math.random() * chars.length));
   }
   captchaCode = code;
   document.getElementById("captchaPreview").textContent = captchaCode;
 }

 // Generate the initial CAPTCHA on page load
 generateCaptcha();

 // Handle the login form submission
 document.getElementById("login-form").addEventListener("submit", async function (event) {
   event.preventDefault();  // Prevent default form submission

   // Validate CAPTCHA
   const captchaInput = document.getElementById("captcha").value;
   if (captchaInput !== captchaCode) {
     swal("CAPTCHA Error", "Incorrect CAPTCHA. Please try again.", "error");
     generateCaptcha();  // Regenerate CAPTCHA
     return;
   }

   const form = document.getElementById("login-form");
   const formData = new FormData(form);

   // Send a POST request to the /login endpoint
   try {
     const response = await fetch("/login", {
       method: "POST",
       body: formData
     });

     if (response.ok) {
       const data = await response.json();
       // Store the JWT token in localStorage
       const token = data.access_token;
       localStorage.setItem('access_token', token);
       // If login is successful, redirect to the dashboard
       window.location.href = "/dashboard";
     } else {
       // Parse the error response and display an alert
       const errorData = await response.json();
       swal("Login Failed", errorData.detail || "Invalid username or password.", "error");
     }
   } catch (error) {
     // Handle network or other errors
     swal("Error", "An error occurred during the login process. Please try again.", "error");
     console.error("Login error:", error);
   }
 });