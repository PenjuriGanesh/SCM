document.getElementById('shipment-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevents the default form submission

    // Collect the form data as an object
    const formData = new FormData(document.getElementById('shipment-form'));

    // Additional Validation Checks
    const sinum = formData.get('shipment_number');
    const cnum = formData.get('container_number');
    const goodsno = formData.get('goods_number');
    const rdetails = formData.get('route_details');
    const gdtypes = formData.get('goods_type');
    const device = formData.get('device_id');
    const exdate = formData.get('expected_delivery_date');
    const ponum = formData.get('po_number');
    const delnum = formData.get('delivery_number');
    const ndcnum = formData.get('ndc_number');
    const bid = formData.get('batch_id');
    const sdesc = formData.get('shipment_description');

    // Basic validation checks
    if (!sinum || !cnum || !goodsno || !rdetails || !gdtypes || !device || !exdate || !ponum || !delnum || !ndcnum || !bid || !sdesc) {
        alert('All fields are required.');
        return;
    }

    // Retrieve the token from localStorage
    const token = localStorage.getItem("access_token");
    if (!token) {
        alert("You need to be logged in to view this page.");
        window.location.href = "/login"; // Redirect to login page
    }
    

    // Send the data to the backend using fetch API
    fetch("/newshipment_user", {
        method: "POST",
        headers: {
            'Authorization': `Bearer ${token}`,  // Add token in Authorization header
            'Content-Type': 'application/json'   // Set Content-Type to JSON
        },
        body: JSON.stringify({
            shipment_number: sinum,
            container_number: cnum,
            goods_number: goodsno,
            route_details: rdetails,
            goods_type: gdtypes,
            device_id: device,
            expected_delivery_date: exdate,
            po_number: ponum,
            delivery_number: delnum,
            ndc_number: ndcnum,
            batch_id: bid,
            shipment_description: sdesc
        })  // Convert the form data to JSON
    })
    .then(async (response) => {
        if (response.ok) {
            alert('Shipment details submitted successfully! Redirecting...');
            window.location.href = "/myshipment"; 
        } else {
            const errorData = await response.json();
            alert(errorData.detail || "Submission failed. Please try again.");
        }
    })
    .catch((error) => {
        alert("An error occurred while submitting the form. Please try again later.");
        console.error("Error:", error);
    });

    // Reset the form after submission
    document.getElementById('shipment-form').reset();
});

// Optionally clear inputs on cancel
function clearinput() {
    document.querySelector("form").reset();
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
  