# Import necessary libraries
import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load your trained model
model = tf.keras.models.load_model('path_to_your_model.h5')

# Function to process images
def process_image(image_path):
    image = cv2.imread(image_path)
    # Preprocess the image (resize, normalize, etc.)
    image = cv2.resize(image, (224, 224))  # Example size
    image = image / 255.0  # Normalize
    return np.expand_dims(image, axis=0)

# Endpoint to analyze crop health
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    image_path = 'path_to_save_image/' + file.filename
    file.save(image_path)

    processed_image = process_image(image_path)
    predictions = model.predict(processed_image)
    
    # Interpret predictions (this will depend on your model)
    result = interpret_predictions(predictions)
    
    return jsonify(result)

def interpret_predictions(predictions):
    # Logic to interpret model predictions
    return {"health_status": "Healthy" if predictions[0] > 0.5 else "Unhealthy"}

if __name__ == '__main__':
    app.run(debug=True)
