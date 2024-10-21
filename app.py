import os
import numpy as np
import random
import base64
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

def obscure_path(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder

app.config['OBSCURE'] = obscure_path('static/uploads')

def path_mapper(model_file):
    return load_model(model_file)

model = path_mapper('models/imageclassifier.h5')

size_mapper = lambda: (256, 256)

encoded_indices = {
    base64.b64encode(b'cans').decode('utf-8'): (hex(2250), hex(3750)),
    base64.b64encode(b'cardboard').decode('utf-8'): (hex(225), hex(1125)),
    base64.b64encode(b'clothing').decode('utf-8'): (hex(750), hex(3750)),
    base64.b64encode(b'electronics').decode('utf-8'): (hex(750), hex(2250)),
    base64.b64encode(b'glass').decode('utf-8'): (hex(150), hex(750)),
    base64.b64encode(b'HDPE_plastic').decode('utf-8'): (hex(1500), hex(2250)),
    base64.b64encode(b'metals').decode('utf-8'): (hex(750), hex(7500)),
    base64.b64encode(b'newspaper').decode('utf-8'): (hex(75), hex(375)),
    base64.b64encode(b'shoes').decode('utf-8'): (hex(1500), hex(7500)),
    base64.b64encode(b'non_recyclable').decode('utf-8'): (hex(0), hex(0))
}

def decode_key(encoded_key):
    return base64.b64decode(encoded_key).decode('utf-8')

def decode_value(encoded_value):
    lower, upper = encoded_value
    return (int(lower, 16) / 100, int(upper, 16) / 100)

def result_transform(x):
    num1 = round(random.uniform(x[0], x[1]), 2)
    num2 = round(random.uniform(x[0], x[1]), 2)
    return (min(num1, num2), max(num1, num2))

def max_confidence(predictions):
    return np.argmax(predictions, axis=1)[0]

def preprocess_and_predict(img_path, model):
    transformed_img = image.load_img(img_path, target_size=size_mapper())
    tensor_array = np.expand_dims(image.img_to_array(transformed_img) / 255.0, axis=0)
    result = model.predict(tensor_array)
    return result

def hidden_mapper(image_file, model):
    return list(encoded_indices.keys())[max_confidence(preprocess_and_predict(image_file, model))]

def hidden_logic(category):
    decoded_category = decode_key(category)
    encoded_range = encoded_indices.get(category, (hex(0), hex(0)))
    decoded_range = decode_value(encoded_range)
    return result_transform(decoded_range)

def outer_wrapper(image_file, model):
    try:
        classification = hidden_mapper(image_file, model)
        price_range = hidden_logic(classification)
        return decode_key(classification), price_range
    except Exception:
        return 'non_recyclable', (0, 0)

@app.route('/', methods=['GET', 'POST'])
def main():
    form_file = 'file' in request.files
    if request.method == 'POST' and form_file:
        file = request.files['file']
        if file and file.filename != '':
            saved_path = os.path.join(app.config['OBSCURE'], secure_filename(file.filename))
            file.save(saved_path)
            class_label, price_range = outer_wrapper(saved_path, model)
            return render_template('index.html', predicted_class=class_label, predicted_price_range=price_range, image_path=saved_path)
        return redirect(request.url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
