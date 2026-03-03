import numpy as np
import tensorflow as tf
from PIL import Image
import io
import json
from tensorflow.keras.applications.efficientnet import preprocess_input

MODEL_PATH = "models/cnn/healthguru_cnn_v1.keras"
CLASS_NAMES_PATH = "models/cnn/class_names.json"

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r") as f:
    CLASS_NAMES = json.load(f)

IMAGE_SIZE = (224, 224)


def predict_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMAGE_SIZE)

    img_array = np.array(image)
    img_array = preprocess_input(img_array)   # 🔥 THIS IS THE FIX
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)

    confidence = float(np.max(predictions))
    class_index = int(np.argmax(predictions))
    label = CLASS_NAMES[class_index]

    return {
        "label": label,
        "confidence": confidence
    }
