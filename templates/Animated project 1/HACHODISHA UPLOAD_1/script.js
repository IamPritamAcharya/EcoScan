document.addEventListener("DOMContentLoaded", function() {
    const uploadButton = document.getElementById('upload-button');
    const uploadForm = document.getElementById('upload-form');
    const uploadContainer = document.querySelector('.upload-container');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');

    // Display chosen file name
    fileInput.addEventListener('change', function() {
        const fileName = fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
        fileNameDisplay.textContent = fileName;
    });

    // Add animation when form is submitted
    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Animate the container on file upload (bounce effect)
        uploadContainer.style.transform = "scale(1.05)";
        setTimeout(() => {
            uploadContainer.style.transform = "scale(1)";
        }, 300);

        // Simulate a successful file upload after 1 second (for demo purposes)
        setTimeout(() => {
            alert('File uploaded successfully!');
        }, 1000);
    });

    // Add animation to the button when clicked
    uploadButton.addEventListener('click', function() {
        uploadButton.classList.add('clicked');
        setTimeout(() => {
            uploadButton.classList.remove('clicked');
        }, 200);
    });
});
function displayFileName() {
    const input = document.getElementById('file-upload');
    const fileNameSpan = document.getElementById('file-name');
    const outputFileName = document.getElementById('output-file-name');

    if (input.files.length > 0) {
        const fileName = input.files[0].name;
        fileNameSpan.textContent = fileName; // Display next to "Choose File"
        outputFileName.textContent = fileName; // Display in the output section
    } else {
        fileNameSpan.textContent = 'No file chosen';
        outputFileName.textContent = 'No file uploaded yet.';
    }
}

