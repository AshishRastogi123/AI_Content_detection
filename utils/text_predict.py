import os
import joblib
import re
import nltk
import gdown
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# =========================
# MODEL DOWNLOAD (Drive)
# =========================

MODEL_PATH = "model/ai_text_detector_model.joblib"
VECTORIZER_PATH = "model/tfidf_vectorizer.joblib"

MODEL_URL = "https://drive.google.com/file/d/1xNGvXdnrj2lzq5CncvEjii4MORxZMiUH/view?usp=sharing"
VECTORIZER_URL = "https://drive.google.com/file/d/1zqrfZJRqwg0FBl7kEJ-6eyQqm-K339Wc/view?usp=sharing"

os.makedirs("models", exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print("Downloading text model...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

if not os.path.exists(VECTORIZER_PATH):
    print("Downloading vectorizer...")
    gdown.download(VECTORIZER_URL, VECTORIZER_PATH, quiet=False)

# =========================
# LOAD MODEL
# =========================

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# =========================
# NLTK SETUP
# =========================

packages = [
    ('tokenizers/punkt', 'punkt'),
    ('corpora/stopwords', 'stopwords'),
    ('corpora/wordnet', 'wordnet')
]

for path, package in packages:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(package)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# =========================
# PREPROCESS FUNCTION
# =========================

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z]', ' ', text)

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)

# =========================
# PREDICTION FUNCTION
# =========================

def predict_text(text):
    text = preprocess_text(text)
    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()

    if prediction == 1:
        label = "AI Generated Text"
    else:
        label = "Human Written Text"

    return label, round(confidence * 100, 2)