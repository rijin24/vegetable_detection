import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
import os

# Set paths
train_dir = 'test/vegetabledataset/train'
val_dir = 'test/vegetabledataset/validation'
img_size = 224
batch_size = 32
num_classes = 15

# Step 1: Data Preprocessing with Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=25,
    zoom_range=0.25,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

val_data = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical'
)

# Step 2: Load MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
base_model.trainable = True  # Unfreeze for fine-tuning


for layer in base_model.layers[:100]:
    layer.trainable = False

# Step 3: Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
output = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

# Step 4: Compile model
model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Learning rate adjustment
lr_callback = ReduceLROnPlateau(monitor='val_accuracy', patience=3, factor=0.5, verbose=1)

# Step 5: Train the model
model.fit(
    train_data,
    validation_data=val_data,
    epochs=20,
    callbacks=[lr_callback]
)

# Step 6: Save model
model.save('vegetable_model_mobilenetv2.h5')

# Step 7: Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('vegetable_model.tflite', 'wb') as f:
    f.write(tflite_model)

print(" Model trained, saved, and converted to TFLite.")
