import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

IMG_SIZE = (224, 224)

# Load model once at startup
model = tf.keras.models.load_model("models/cnn/food_mobilenet_model.keras")

class_names = ['ice_cream', 'pancake', 'pizza', 'spaghetti', 'sushi']

def predict_image(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    
    predicted_class = class_names[predicted_index]
    confidence = float(np.max(predictions))

    return predicted_class, confidence
