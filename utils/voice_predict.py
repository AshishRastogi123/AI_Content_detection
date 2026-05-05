import os
import joblib
import librosa
import numpy as np
import gdown

# =========================
# MODEL DOWNLOAD (Drive)
# =========================

MODEL_PATH = "model/voice_detection_model.pkl"
MODEL_URL = "https://drive.google.com/file/d/1bs9E8v6-G8QvQGMQHgHAVbBFcprX-Q9V/view?usp=sharing"

os.makedirs("models", exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("Downloading voice model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# =========================
# LOAD MODEL
# =========================

model = joblib.load(MODEL_PATH)

# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(file_path):
    audio, sr = librosa.load(file_path, sr=22050)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

    mfcc_scaled = np.mean(mfcc.T, axis=0)

    return mfcc_scaled.reshape(1, -1)

# =========================
# PREDICTION
# =========================

def predict_voice(file_path):
    features = extract_features(file_path)

    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max()

    if prediction == 1:
        label = "AI Generated Voice"
    else:
        label = "Human Voice"

    return label, round(confidence * 100, 2)