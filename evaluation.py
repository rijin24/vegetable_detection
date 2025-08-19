import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image


model = tf.keras.models.load_model('vegetable_recognition_model.keras')


class_names = ['Bean', 'Broccoli', 'Carrot', 'Cauliflower', 'Bitter_Gourd',
               'Bottle_Gourd', 'Brinjal', 'Cabbage', 'Capsicum', 'Cucumber',
               'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']

# Path to validation folder
val_dir = 'test/vegetabledataset/validation'

# Counters for accuracy calculation
correct = 0
total = 0

for class_name in class_names:
    class_path = os.path.join(val_dir, class_name)
    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)

        # Load and preprocess image with input size matching your model (224x224)
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize if done during training
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict the class
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions)]

        # Compare predicted and true class to update counters
        if predicted_class == class_name:
            correct += 1
        total += 1

accuracy = correct / total if total > 0 else 0
print(f"Validation accuracy: {accuracy * 100:.2f}%")
