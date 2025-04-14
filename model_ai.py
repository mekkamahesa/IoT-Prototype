import tensorflow as tf
import numpy as np
from PIL import Image

model = tf.keras.models.load_model("model_sampah.h5")
labels = ['Organik', 'Anorganik', 'Plastik']

def classify_image(img_path):
    img = Image.open(img_path).resize((224, 224))
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    prediction = model.predict(img_array)
    return labels[np.argmax(prediction)]