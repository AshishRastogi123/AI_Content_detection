import os
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
import gdown

# ====== MODEL DOWNLOAD (only first time) ======
MODEL_PATH = "model/deepfake_model.h5"

DRIVE_URL = "https://drive.google.com/uc?export=download&id=1RSncALRxLA3vV4tf15ng8CJ0YnfjcsJO"

if not os.path.exists(MODEL_PATH):
    os.makedirs("models", exist_ok=True)
    print("Downloading model from Google Drive...")
    gdown.download(DRIVE_URL, MODEL_PATH, quiet=False)

# ====== LOAD MODEL ======
model = load_model(MODEL_PATH, compile=False)


# ====== PREPROCESS FUNCTION ======
def preprocess_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((128, 128))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# ====== PREDICTION FUNCTION ======
def predict_image(img_path):
    processed = preprocess_image(img_path)

    prediction = model.predict(processed)[0][0]

    if prediction > 0.5:
        label = "Fake Image"
        confidence = prediction
    else:
        label = "Real Image"
        confidence = 1 - prediction

    confidence = round(float(confidence), 2)

    return label, confidence