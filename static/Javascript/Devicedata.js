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

// Fetch and display device data
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        alert("You need to login to access this page.");
        window.location.href = "/login";
        return;
    }

    // Function to get authorization headers
    function getAuthHeaders() {
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
})
//     // Fetch device data from Kafka API
//     fetch('/devicedata', {  // Endpoint that returns data from Kafka
//         method: 'GET',
//         headers: getAuthHeaders()
//     })
//     .then(response => response.json())
//     .then(data => {
//         const tableBody = document.querySelector('#device-data-table tbody');

//         // Clear any previous data
//         tableBody.innerHTML = '';

//         // Populate table with the fetched data
//         data.forEach(device => {
//             const row = document.createElement('tr');

//             // Create table cells for each device property
//             const deviceIdCell = document.createElement('td');
//             deviceIdCell.textContent = device.device_id;
//             row.appendChild(deviceIdCell);

//             const batteryLevelCell = document.createElement('td');
//             batteryLevelCell.textContent = device.battery_level;
//             row.appendChild(batteryLevelCell);

//             const sensorTempCell = document.createElement('td');
//             sensorTempCell.textContent = device.sensor_temperature;
//             row.appendChild(sensorTempCell);

//             const routeFromCell = document.createElement('td');
//             routeFromCell.textContent = device.route_from;
//             row.appendChild(routeFromCell);

//             const routeToCell = document.createElement('td');
//             routeToCell.textContent = device.route_to;
//             row.appendChild(routeToCell);

//             // Append the row to the table body
//             tableBody.appendChild(row);
//         });
//     })
//     .catch(error => {
//         console.error('Error fetching device data:', error);
//         document.getElementById('error_message').textContent = 'Failed to load device data. Please try again later.';
//     });
// });
