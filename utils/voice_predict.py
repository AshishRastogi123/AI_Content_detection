import joblib
import librosa
import numpy as np


# load trained model
model = joblib.load("models/voice_detection_model.pkl")


# -------------------------
# Feature Extraction
# -------------------------

def extract_features(file_path):

    audio, sr = librosa.load(file_path, sr=22050)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

    mfcc_scaled = np.mean(mfcc.T, axis=0)

    return mfcc_scaled.reshape(1,-1)


# -------------------------
# Prediction
# -------------------------

def predict_voice(file_path):

    features = extract_features(file_path)

    prediction = model.predict(features)[0]

    confidence = model.predict_proba(features).max()

    if prediction == 1:
        label = "AI Generated Voice"
    else:
        label = "Human Voice"

    return label, round(confidence*100,2)