let captchaCode = "";

// Function to generate a random CAPTCHA code
function generateCaptcha() {
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let code = "";
  for (let i = 0; i < 6; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  captchaCode = code;
  document.getElementById("captchaPreview").textContent = captchaCode; // Display the CAPTCHA code
}

// Generate the initial CAPTCHA on page load
window.addEventListener('load', () => {
  generateCaptcha(); // Generate the CAPTCHA once the page is fully loaded
});

// Handle the login form submission
document.getElementById("login-form").addEventListener("submit", async function (event) {
  event.preventDefault(); // Prevent default form submission

  // Validate CAPTCHA
  const captchaInput = document.getElementById("captcha").value;

  // Check if CAPTCHA input is correct
  if (captchaInput !== captchaCode) {
    console.log("Incorrect CAPTCHA");

    // Display the CAPTCHA error message in the HTML
    const captchaErrorElement = document.getElementById("captchaError");
    captchaErrorElement.style.display = "block";

    return;
  }


  const form = document.getElementById("login-form");
  const formData = new FormData(form);

  try {
    const response = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      // Store the JWT token in localStorage
      const token = data.access_token;
      localStorage.setItem("access_token", token);
      // If login is successful, redirect to the dashboard
      window.location.href = "/dashboard";
    } else {
      const errorData = await response.json();
      // Display error message directly on the page
      displayError(errorData.detail || "Invalid username or password.");
    }
  } catch (error) {
    // Handle network or other errors
    displayError("An error occurred during the login process. Please try again.");
    console.error("Login error:", error);
  }
});

// Function to display the error message directly on the page
function displayError(message) {
  const errorMessage = document.createElement("div");
  errorMessage.classList.add("form-alert", "alert-error");
  errorMessage.textContent = message;
  const form = document.getElementById("login-form");
  form.insertBefore(errorMessage, form.firstChild); // Display error at the top of the form

  // Automatically hide the error after 5 seconds
  setTimeout(() => {
    errorMessage.style.display = "none";
  }, 5000);
}
