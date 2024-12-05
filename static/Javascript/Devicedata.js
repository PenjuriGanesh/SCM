document.addEventListener("DOMContentLoaded", function() {

    // Function to get authorization headers
    function getAuthHeaders() {
        const token = localStorage.getItem("access_token");
        if (!token) {
            alert("Authentication required. Please log in.");
            window.location.href = "/login";
            return;
        }
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    

    // Fetch device data from the backend
    fetch("/devicedata", {
        method: "GET",
        headers: getAuthHeaders() // This sends the JWT token in the header
    })
    .then(response => {
        // Check if the response is successful
        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
                alert("You are not authorized to view this page. Please login.");
                window.location.href = "/login";
            } else {
                // Handle other error cases
                alert("Error: Unable to fetch device data.");
                console.error("Error fetching data:", response.statusText);
            }
            throw new Error('Unauthorized or failed response');
        }
    
        // Check if the content type is JSON before parsing
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/json")) {
            return response.json(); // Parse JSON response
        } 
    })
    .then(data => {
        if (data && Array.isArray(data)) {
            if (data.length === 0) {
                document.getElementById("error_message").textContent = "No device data found.";
            } else {
                // Populate table with data
                const tableBody = document.querySelector("#device-data-table tbody");
                data.forEach(device => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${device.Device_Id}</td>
                        <td>${device.Battery_Level}</td>
                        <td>${device.First_Sensor_temperature}</td>
                        <td>${device.Route_From}</td>
                        <td>${device.Route_To}</td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        } 
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred: " + error.message);
    }
);
    
})

    // Logout function
    function logout(event) {
        event.preventDefault();  // Prevent the default behavior (like page redirect)

        localStorage.removeItem("access_token");

        // Send a request to the backend to delete the cookie
        fetch("/logout", {
            method: "POST",
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
    };
