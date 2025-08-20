document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('captureBtn');
    const stopBtn = document.getElementById('stopBtn');
    const resultImage = document.getElementById('resultImage');
    
    captureBtn.addEventListener('click', function() {
        // Send request to detect faces
        fetch('/detect_faces', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Display the processed image
                resultImage.innerHTML = `<img src="data:image/jpeg;base64,${data.image}" alt="Processed Image">`;
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing the image.');
        });
    });
    
    stopBtn.addEventListener('click', function() {
        // Stop the camera
        fetch('/stop_camera')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Camera stopped successfully.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});