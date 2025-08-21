import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
import os

# Dataset directories
train_path = 'test/vegetabledataset/train'
valid_path = 'test/vegetabledataset/validation'
image_dim = 224
batch_sz = 32
class_count = 15

# ===============================
# 1. Data Augmentation & Generators
# ===============================
train_gen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=30,
    zoom_range=0.2,
    width_shift_range=0.15,
    height_shift_range=0.15,
    horizontal_flip=True
)

valid_gen = ImageDataGenerator(rescale=1.0/255)

train_loader = train_gen.flow_from_directory(
    train_path,
    target_size=(image_dim, image_dim),
    batch_size=batch_sz,
    class_mode='categorical'
)

valid_loader = valid_gen.flow_from_directory(
    valid_path,
    target_size=(image_dim, image_dim),
    batch_size=batch_sz,
    class_mode='categorical'
)

# ===============================
# 2. Load Pre-trained MobileNetV2
# ===============================
mobilenet_base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(image_dim, image_dim, 3))
mobilenet_base.trainable = True  # enable fine-tuning

# Freeze the first set of layers
for lyr in mobilenet_base.layers[:100]:
    lyr.trainable = False

# ===============================
# 3. Add Classification Layers
# ===============================
net = mobilenet_base.output
net = GlobalAveragePooling2D()(net)
net = Dense(256, activation='relu')(net)
net = Dropout(0.3)(net)
net = Dense(128, activation='relu')(net)
net = Dropout(0.3)(net)
final_output = Dense(class_count, activation='softmax')(net)

veg_model = Model(inputs=mobilenet_base.input, outputs=final_output)

# ===============================
# 4. Compile Model
# ===============================
veg_model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Learning rate schedule callback
lr_scheduler = ReduceLROnPlateau(monitor='val_accuracy', patience=3, factor=0.5, verbose=1)

# ===============================
# 5. Train Model
# ===============================
veg_model.fit(
    train_loader,
    validation_data=valid_loader,
    epochs=20,
    callbacks=[lr_scheduler]
)

# ===============================
# 6. Save Model
# ===============================
veg_model.save('vegetable_model_mobilenetv2.h5')

# ===============================
# 7. Convert to TensorFlow Lite
# ===============================
tflite_converter = tf.lite.TFLiteConverter.from_keras_model(veg_model)
tflite_model = tflite_converter.convert()

with open('vegetable_model.tflite', 'wb') as file:
    file.write(tflite_model)

print("Training complete. Model saved and converted to TFLite.")
