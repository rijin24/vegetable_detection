from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np

mobile_bp = Blueprint('mobile', __name__)
model = load_model('vegetable_model_mobilenetv2.h5')

class_names = [
    'Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum',
    'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potatoe', 'Pumpkin', 'Radish', 'Tomato'
]
recipes = {
    'carrot': 'Try making carrot halwa!',
    'potato': 'Try mashed potatoes or fries!',
    'tomato': 'Tomato soup is a classic!',
}

@mobile_bp.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img = img.resize((224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    class_name = class_names[class_index]
    confidence = float(np.max(predictions))
    recipe = recipes.get(class_name.lower(), "No recipe available.")

    return jsonify({
        'vegetable': class_name,
        'confidence': confidence,
        'recipe': recipe
    })
