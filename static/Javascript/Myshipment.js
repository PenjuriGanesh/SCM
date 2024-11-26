// Get all the sidebar links
const sidebarLinks = document.querySelectorAll('.sidebar-links li a');

// Function to set the active link based on the current URL
function setActiveLink() {
    sidebarLinks.forEach(link => {
        link.classList.remove('active'); // Remove active class from all links
        if (window.location.pathname.includes(link.getAttribute('href'))) {
            link.classList.add('active'); // Add active class to the matching link
        }
    });
}

function setupSidebar() {
    setActiveLink(); // Set the active link based on the current URL

    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // When a sidebar link is clicked, set it as active
            setActiveLink();
        });
    });
}

async function fetchShipments() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        alert("You need to be logged in to view your shipments.");
        window.location.href = "/login"; // Redirect to login page if no token
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Shipments data:", data);
            // Optionally, update the page content with the fetched data
        } else {
            const errorData = await response.json();
            alert(errorData.detail || "Failed to fetch shipments.");
        }
    } catch (error) {
        console.error("Error fetching shipments:", error);
        alert("An error occurred while fetching shipments.");
    }
}

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
  

// Automatically run the authentication check and other functions on page load
window.addEventListener("load", function () {
    setupSidebar();  // Initialize the sidebar and set the active link
    fetchShipments(); // Fetch shipments after ensuring authentication
    logout()
});