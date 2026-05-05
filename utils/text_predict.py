import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


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
# load model
model = joblib.load(open("models/ai_text_detector_model.joblib", "rb"))

# load vectorizer
vectorizer = joblib.load(open("models/tfidf_vectorizer.joblib", "rb"))

# nltk setup
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


# ----------------------------
# Text Preprocessing
# ----------------------------

def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'[^a-zA-Z]', ' ', text)

    tokens = word_tokenize(text)

    tokens = [word for word in tokens if word not in stop_words]

    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return " ".join(tokens)


# ----------------------------
# Prediction Function
# ----------------------------

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