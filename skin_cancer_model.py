import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the trained model
model_path = r"D:\ITSOLERA Project 2\skin_cancer_detection_model.keras"
model = tf.keras.models.load_model(model_path)

# Function to preprocess the image before prediction
def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))  # Resize image to match model's input shape
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize pixel values to [0, 1]
    return img_array

# Function to predict skin cancer using the trained model
def predict_skin_cancer(image_path):
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)

        # Make prediction
        prediction = model.predict(processed_image)
        confidence = float(np.max(prediction))  # Get confidence score

        # Assuming binary classification: 0 -> Benign, 1 -> Malignant
        if np.argmax(prediction) == 0:
            result = 'Benign'
        else:
            result = 'Malignant'

        return result, confidence

    except Exception as e:
        print(f"Error during prediction: {e}")
        return "Error", 0.0
