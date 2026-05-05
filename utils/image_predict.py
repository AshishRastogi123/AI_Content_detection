import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# model load
model = load_model("models/deepfake_model.h5")


def preprocess_image(img_path):

    # image open and resize
    img = Image.open(img_path).convert("RGB")
    img = img.resize((128, 128))

    # convert to numpy array
    img = np.array(img)

    # normalization
    img = img / 255.0

    # add batch dimension
    img = np.expand_dims(img, axis=0)

    return img


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