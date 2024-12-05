document.addEventListener('DOMContentLoaded', () => {
    // Event listener for form submission
    document.getElementById('shipment-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevents the default form submission

        // Collect the form data into an object
        const formData = {
            shipment_number: parseInt(document.getElementById('sinum').value),
            container_number: parseInt(document.getElementById('cnum').value),
            goods_number: parseInt(document.getElementById('goodsno').value),
            route_details: document.getElementById('rdetails').value,
            goods_type: document.getElementById('gdtypes').value,
            device_id: parseInt(document.getElementById('device').value),
            expected_delivery_date: document.getElementById('exdate').value,
            po_number: parseInt(document.getElementById('ponum').value),
            delivery_number: parseInt(document.getElementById('delnum').value),
            ndc_number: parseInt(document.getElementById('ndcnum').value),
            batch_id: parseInt(document.getElementById('bid').value),
            shipment_description: document.getElementById('sdesc').value
        };

        // Validate that shipment number is exactly 7 digits
        if (formData.shipment_number.toString().length !== 7) {
            alert("Shipment number must be exactly 7 digits.");
            return; // Prevent form submission
        }

        // Get the token from localStorage
        const token = localStorage.getItem("access_token");
        
        // Send the data to the backend using fetch API
        fetch("/newshipment_user", {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,  // Add token in Authorization header
                'Content-Type': 'application/json'   // Set Content-Type to JSON
            },
            body: JSON.stringify(formData)  // Send the data as JSON
        })
        .then(async (response) => {
            if (response.ok) {
                alert('Shipment details submitted successfully!');
                document.getElementById('shipment-form').reset();  // Reset the form after submission
                window.location.href = "/myshipment";  // Redirect after success
            } else {
                const errorData = await response.json();
                alert(errorData.error_message || "Submission failed. Please try again.");
            }
        })
        .catch((error) => {
            alert("An error occurred while submitting the form. Please try again later.");
            console.error("Error:", error);
        });
    });

    document.getElementById('canbtn').addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default behavior of the button (if it's a submit)
        document.getElementById('shipment-form').reset();  // Reset the form
    });
});

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
}
