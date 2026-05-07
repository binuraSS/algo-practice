import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os

# Create dummy data (since we don't have real images locally)
# This creates patterns that mimic fruits
print("Creating training data...")

# Generate fake fruit images (100x100 RGB)
x_train = np.random.rand(1000, 100, 100, 3).astype(np.float32)
y_train = np.random.randint(0, 4, (1000, 1))

x_test = np.random.rand(200, 100, 100, 3).astype(np.float32)
y_test = np.random.randint(0, 4, (200, 1))

# Convert labels to categorical
y_train = keras.utils.to_categorical(y_train, 4)
y_test = keras.utils.to_categorical(y_test, 4)

# Build model
model = keras.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(100, 100, 3)),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print("Training...")
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Save
model.save('simple_fruit_model.keras')
print("Model saved as simple_fruit_model.keras")