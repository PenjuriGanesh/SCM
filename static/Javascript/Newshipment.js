document.addEventListener('DOMContentLoaded', () => {
    // Get the response message element
    const responseMessage = document.getElementById('response-message');

    // Event listener for form submission
    document.getElementById('shipment-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevents the default form submission

        // Collect the form data 
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

        // Validate that shipment number, container number, PO number, and batch ID are exactly 7 digits
        if (formData.shipment_number.toString().length !== 7) {
            responseMessage.textContent = "Shipment number must be exactly 7 digits.";
            responseMessage.classList.remove("green"); // Remove any green class (success)
            responseMessage.classList.add("red"); // Add red class (error)
            responseMessage.style.display = "block"; // Display the error message
            return; // Prevent form submission
        }

        if (formData.container_number.toString().length !== 7) {
            responseMessage.textContent = "Container number must be exactly 7 digits.";
            responseMessage.classList.remove("green"); 
            responseMessage.classList.add("red"); 
            responseMessage.style.display = "block"; 
            return; 
        }

        if (formData.po_number.toString().length !== 7) {
            responseMessage.textContent = "PO number must be exactly 7 digits.";
            responseMessage.classList.remove("green"); 
            responseMessage.classList.add("red"); 
            responseMessage.style.display = "block"; 
            return; 
        }

        if (formData.batch_id.toString().length !== 7) {
            responseMessage.textContent = "Batch ID must be exactly 7 digits.";
            responseMessage.classList.remove("green"); 
            responseMessage.classList.add("red"); 
            responseMessage.style.display = "block"; 
            return; 
        }

        // Hide any error message if validation passes
        responseMessage.style.display = "none";

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
                responseMessage.textContent = 'Shipment details submitted successfully!';
                responseMessage.classList.remove("red"); 
                responseMessage.classList.add("green"); 
                responseMessage.style.display = "block"; 
                document.getElementById('shipment-form').reset();  
                window.location.href = "/myshipment";  
            } else {
                const errorData = await response.json();
                responseMessage.textContent = errorData.error_message || "Submission failed. Please try again.";
                responseMessage.classList.remove("green"); 
                responseMessage.classList.add("red"); 
                responseMessage.style.display = "block"; 
            }
        })
        .catch((error) => {
            responseMessage.textContent = "An error occurred while submitting the form. Please try again later.";
            responseMessage.classList.remove("green");
            responseMessage.classList.add("red");
            responseMessage.style.display = "block"; 
            console.error("Error:", error);
        });
    });

    // Event listener for the cancel button
    document.getElementById('canbtn').addEventListener('click', function(event) {
        event.preventDefault();  // Prevent default behavior of the button (if it's a submit)
        document.getElementById('shipment-form').reset();  
        responseMessage.style.display = "none"; 
    });
});

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
    });
}
