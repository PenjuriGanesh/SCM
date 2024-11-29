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

    // Fetch device data from the backend
    fetch("/devicedata", {
        method: "GET",
        headers: getAuthHeaders() // This sends the JWT token in the header
    })
    .then(response => response.json())
    .then(data => {
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
    })
    
});
