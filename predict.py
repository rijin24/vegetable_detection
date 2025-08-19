import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import sys
import os

# -----------------------------
#  Settings
MODEL_PATH = 'vegetable_model_mobilenetv2.h5'
IMG_SIZE = 224


class_names = [
    'Bean', 'Bitter_Gourd' , 'Botle_Gourd' , 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum',
    'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato',
    'Pumpkin', 'Radish', 'Tomato',
]
# -----------------------------

def load_and_prepare_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

def main(img_path):
    # Check model exists
    if not os.path.exists(MODEL_PATH):
        print(f" Model file not found: {MODEL_PATH}")
        sys.exit(1)

    print("Loading model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print(f"Preparing image: {img_path}")
    img_array = load_and_prepare_image(img_path)

    print("Predicting...")
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = predictions[0][predicted_index]

    predicted_class = class_names[predicted_index]

    print(f"\nPrediction complete!")
    print(f"Predicted class index: {predicted_index}")
    print(f"Predicted class name : {predicted_class}")
    print(f"Confidence           : {confidence:.4f}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    test_image_path = sys.argv[1]
    if not os.path.exists(test_image_path):
        print(f" Image file not found: {test_image_path}")
        sys.exit(1)

    main(test_image_path)
