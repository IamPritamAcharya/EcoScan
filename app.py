import os
import numpy as np
import random
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODEL_PATH = 'models/imageclassifier.h5'
model = load_model(MODEL_PATH)

img_size = (256, 256)  

class_names = ['cans', 'cardboard', 'clothing', 'electronics', 'glass', 'HDPE_plastic', 'metals', 'newspaper', 'shoes']

class_price_ranges = {
    'newspaper': (0.75, 3.75),
    'cardboard': (2.25, 11.25),
    'PET_plastic': (11.25, 18.75),
    'HDPE_plastic': (15, 22.50),
    'cans': (22.50, 37.50),
    'metals': (7.50, 75),
    'glass': (1.50, 7.50),
    'clothing': (7.50, 37.50),
    'shoes': (15, 75),
    'electronics': (7.50, 22.50),
    'non_recyclable': (0, 0)
}

def generate_random_price_range(price_range):
    lower, upper = price_range
    num1 = round(random.uniform(lower, upper), 2)
    num2 = round(random.uniform(lower, upper), 2)
    return (num1, num2) if num1 < num2 else (num2, num1)

def predict_class(img_path, model):
    try:
        img = image.load_img(img_path, target_size=img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  
        img_array = img_array / 255.0 

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions, axis=1)[0]  
        predicted_class_label = class_names[predicted_class_index]  

        predicted_price_range = class_price_ranges.get(predicted_class_label, (0, 0))

        random_price_range = generate_random_price_range(predicted_price_range)

        return predicted_class_label, random_price_range
    except Exception as e:
        print(f"Error predicting class: {e}")
        return 'non_recyclable', (0, 0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            predicted_class, predicted_price_range = predict_class(file_path, model)

            return render_template('index.html', predicted_class=predicted_class, predicted_price_range=predicted_price_range, image_path=file_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
