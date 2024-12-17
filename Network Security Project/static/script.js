document.getElementById('sendTrafficButton').addEventListener('click', function() {
    // Get selected traffic types from the multi-select dropdown
    const selectedTrafficTypes = Array.from(document.getElementById('trafficType').selectedOptions)
                                       .map(option => option.value);

    // Send selected traffic types to the Flask backend
    fetch('/api/send_traffic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "traffic_types": selectedTrafficTypes })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('responseMessage').textContent = data.error;
        } else {
            document.getElementById('responseMessage').textContent = data.message;
            document.getElementById('trafficGraphImg').src = 'data:image/png;base64,' + data.img_data;
            updateTrafficDetails(data.details);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to update traffic details on the page
function updateTrafficDetails(details) {
    const detailsList = document.getElementById('trafficInfoList');
    detailsList.innerHTML = '';  // Clear previous details

    details.forEach(detail => {
        const listItem = document.createElement('li');
        listItem.textContent = detail;
        detailsList.appendChild(listItem);
    });
}
