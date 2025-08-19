from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np
import pandas as pd
import os
import tensorflow as tf

# Define Blueprint
mobile_bp = Blueprint('mobile', __name__)

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='vegetable_model.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class labels
class_names = [
    'Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum',
    'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potatoe', 'Pumpkin', 'Radish', 'Tomato'
]

# Optional default recipes
recipes = {
    'carrot': 'Try making carrot halwa!',
    'potato': 'Try mashed potatoes or fries!',
    'tomato': 'Tomato soup is a classic!',
}

# 🔍 Image prediction endpoint using TFLite
@mobile_bp.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Set tensor and invoke interpreter
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    class_index = int(np.argmax(output_data))
    class_name = class_names[class_index]
    confidence = float(np.max(output_data))
    recipe = recipes.get(class_name.lower(), "No recipe available.")

    return jsonify({
        'vegetable': class_name,
        'confidence': confidence,
        'recipe': recipe
    })


# 🥘 Recipe retrieval endpoint
@mobile_bp.route('/get_recipes', methods=['GET'])
def get_recipes():
    vegetable = request.args.get('vegetable')
    if not vegetable:
        return jsonify({'error': 'Missing vegetable name'}), 400

    # Construct full path to Excel file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, '..', 'test', 'vegetabledataset', 'recipe_data', 'sample_dataset.xlsx')

    if not os.path.exists(excel_path):
        return jsonify({'error': 'Recipe dataset not found'}), 404

    try:
        df = pd.read_excel(excel_path)

        # Ensure required columns exist
        required_columns = ['RECIPENAME', 'INGREDIENTS', 'RECIPEURL', 'DESCRIPTION']
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'Missing required columns in dataset'}), 500

        # Filter rows where the ingredient string contains the vegetable name (case-insensitive)
        matching_recipes = df[df['INGREDIENTS'].str.contains(vegetable, case=False, na=False)]

        if matching_recipes.empty:
            return jsonify({'message': f'No recipes found containing {vegetable}'}), 200

        # Convert to list of dicts
        recipe_list = matching_recipes[required_columns].to_dict(orient='records')

        return jsonify({'recipes': recipe_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 📝 Get ingredients for a recipe
@mobile_bp.route('/get_ingredients', methods=['GET'])
def get_ingredients():
    recipe_name = request.args.get('recipe_name')
    if not recipe_name:
        return jsonify({'error': 'Missing recipe_name'}), 400

    # Construct full path to Excel file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(base_dir, '..', 'test', 'vegetabledataset', 'recipe_data', 'sample_dataset.xlsx')

    if not os.path.exists(excel_path):
        return jsonify({'error': 'Recipe dataset not found'}), 404

    try:
        df = pd.read_excel(excel_path)

        # Ensure required columns exist
        if 'RECIPENAME' not in df.columns or 'INGREDIENTS' not in df.columns:
            return jsonify({'error': 'Missing required columns in dataset'}), 500

        # Match recipe by name (case-insensitive)
        matched_recipe = df[df['RECIPENAME'].str.lower() == recipe_name.strip().lower()]

        if matched_recipe.empty:
            return jsonify({'error': 'Recipe not found'}), 404

        ingredients_str = matched_recipe.iloc[0]['INGREDIENTS']
        ingredients_list = [i.strip() for i in ingredients_str.split(',') if i.strip()]

        return jsonify({'ingredients': ingredients_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
