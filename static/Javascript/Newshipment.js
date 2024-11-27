document.addEventListener('DOMContentLoaded',()=>{
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
        const formdata = new FormData()
        for (let key in formData) {
            formdata.append(key, formData[key]);
            console.log(key,formData[key],typeof formData[key])
        }
        // Basic validation checks for required fields
        // for (let key in Object.entries(formData)) {
        //     console.log('inside for ',key)
        //     if (!formData[key]) {
        //         alert('All fields are required.');
        //         return;
        //     }
        // }
    
        // Retrieve the token from localStorage
        const token = localStorage.getItem("access_token");
        if (!token) {
            alert("You need to be logged in to submit this form.");
            window.location.href = "/login"; // Redirect to login page
            return;
        }
    
        // Send the data to the backend using fetch API
        fetch("/newshipment_user", {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,  // Add token in Authorization header
                'Content-Type': 'application/json'   // Set Content-Type to JSON
            },
          
        })
        .then(async (response) => {
            if (response.ok) {
                alert('Shipment details submitted successfully! Redirecting...');
                window.location.href = "/myshipment";  // Redirect after success
            } else {
                const errorData = await response.json();
                alert("Submission failed. Please try again.");
            }
        })
        .catch((error) => {
            alert("An error occurred while submitting the form. Please try again later.");
            console.error("Error:", error);
        });
    
        // Reset the form after submission
        document.getElementById('shipment-form').reset();
    });
    
})

// Optionally clear inputs on cancel
function clearinput() {
    document.querySelector("form").reset();
}

// Handle logout (if used on the same page)
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
