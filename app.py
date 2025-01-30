from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
import os

app = Flask(__name__)

base_path = '/app/saved_model/'

MODEL_PATH = base_path + 'finalmodel.hdf5' 

model = load_model(MODEL_PATH)
print("Model loaded successfully.")

class_labels = ['Benign', 'In Situ', 'Invasive', 'Normal']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file:
        filepath = os.path.join( base_path, file.filename)
        file.save(filepath)

        img = load_img( filepath, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = class_labels[np.argmax(predictions[0])]
        confidence = np.max(predictions[0]) * 100

        os.remove(filepath)

        return jsonify({
            "prediction": predicted_class,
            "confidence": f"{confidence:.2f}%"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)