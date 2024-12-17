document.getElementById('sendTrafficButton').addEventListener('click', function() {
    // Get the selected traffic type from the dropdown
    const trafficType = document.getElementById('trafficType').value;

    // Send traffic type to the Flask backend
    fetch('/api/send_traffic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "traffic_type": trafficType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('responseMessage').textContent = data.error;
        } else {
            document.getElementById('responseMessage').textContent = data.message;
            document.getElementById('trafficGraphImg').src = 'data:image/png;base64,' + data.img_data;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
