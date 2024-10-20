function processImage() {
    const imageInput = document.getElementById('imageInput');
    const imagePreview = document.getElementById('imagePreview');
    const detectedObjectsDiv = document.getElementById('detectedObjects');

    if (imageInput.files && imageInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            // Display image in preview
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';

            // Call Python function from PyScript
            let imagePath = imageInput.files[0].name;  // Get the image file name
            pyscript.run(`classify_image('${imagePath}')`);  // Trigger Python function in main.py
        }

        reader.readAsDataURL(imageInput.files[0]);
    }
}
