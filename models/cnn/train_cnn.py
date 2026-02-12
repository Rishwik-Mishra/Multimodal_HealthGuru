import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import os

#We are telling TensorFlow where images are stored.
train_dir = os.path.join("data", "food_images", "train")
val_dir = os.path.join("data", "food_images", "val")

#Loading Dataset Properly
IMG_SIZE = (128, 128)
BATCH_SIZE = 16

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)
class_names = train_dataset.class_names
print("Detected Classes:", class_names)

#Normalizing the images
normalization_layer = layers.Rescaling(1./255)

train_dataset = train_dataset.map(lambda x, y: (normalization_layer(x), y))
val_dataset = val_dataset.map(lambda x, y: (normalization_layer(x), y))

#Building the CNN Model
model = models.Sequential([
    
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),

    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),

    layers.Dense(5, activation='softmax')
])

#compiling the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

#Training the model
history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10
)

#saving the model
model.save("models/cnn/food_cnn_model.keras")
