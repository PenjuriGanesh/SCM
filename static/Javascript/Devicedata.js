// Check if the user is logged in (check for the presence of the access_token in localStorage)
window.addEventListener('load', function() {
    const accessToken = localStorage.getItem("access_token");

    // If there's no access token, show an alert and redirect to the login page
    if (accessToken === null) {
        alert("To view this page, you need to log in.");
        window.location.href = "/login";  // Redirect to the login page
    } else {
        console.log("Access token found. User is logged in.");
    }
});

// Function to logout and clear the token
function logout(event) {
    event.preventDefault();  // Prevent the default behavior (like page redirect)

    // Remove the JWT token from localStorage
    localStorage.removeItem("access_token");

    // Send a request to the backend to delete the cookie
    fetch("/logout", {
        method: "POST",  // Make a POST request to the /logout endpoint
        credentials: "same-origin",  // Ensure cookies are sent with the request
        headers: {
            "Content-Type": "application/json"  // Ensure the request is in JSON format
        }
    })
    .then(response => {
        if (response.ok) {
            // If logout is successful, redirect to login page
            window.location.href = "/login";
        } else {
            throw new Error("Logout failed");
        }
    })
    .catch(error => {
        console.error("Logout error:", error);
        alert("Error logging out. Please try again.");
    });
}
