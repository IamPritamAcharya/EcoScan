import os
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the saved model
model = load_model('models/imageclassifier.h5')

# Set the image size and class names
img_size = (256, 256)  # Same size used during training
class_names = os.listdir('data')  # The class names based on the folders in 'data'

# Create a directory for uploads if not exists
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def split_image_into_patches(image, patch_size):
    """
    Split the image into patches of size (patch_size, patch_size).
    """
    patches = []
    img_height, img_width, _ = image.shape
    for y in range(0, img_height, patch_size[1]):
        for x in range(0, img_width, patch_size[0]):
            patch = image[y:y+patch_size[1], x:x+patch_size[0]]
            if patch.shape[:2] == patch_size:
                patches.append(patch)
    return patches

def identify_objects_in_image(image_path, model, img_size):
    """
    Identifies objects in an image by splitting it into patches and running each patch through the model.
    """
    # Load and preprocess the image
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Split the image into smaller patches
    patches = split_image_into_patches(image_rgb, img_size)
    
    detected_classes = []
    
    # Iterate through patches and make predictions
    for patch in patches:
        # Resize patch to match the input shape of the model
        resized_patch = cv2.resize(patch, img_size)
        resized_patch = np.expand_dims(resized_patch / 255.0, axis=0)  # Normalize and add batch dimension
        
        # Predict the class probabilities for the patch
        predictions = model.predict(resized_patch)
        predicted_class = np.argmax(predictions, axis=1)[0]  # Get the class with the highest probability
        predicted_label = class_names[predicted_class]
        
        # If the class is not already detected, add it to the detected_classes list
        if predicted_label not in detected_classes:
            detected_classes.append(predicted_label)
    
    return detected_classes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an image was uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Save the file to the upload folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Detect objects in the image
            detected_objects = identify_objects_in_image(file_path, model, img_size)
            
            # Render the result in the HTML template
            return render_template('index.html', detected_objects=detected_objects, image_path=file_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
