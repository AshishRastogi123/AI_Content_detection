from flask import Flask, render_template, request
import os
import warnings

warnings.filterwarnings("ignore")

# =========================
# APP INIT
# =========================
app = Flask(__name__, static_folder="statics", static_url_path="/statics")

# =========================
# FOLDER SETUP (IMPORTANT)
# =========================
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# =========================
# IMPORTS (AFTER APP INIT)
# =========================
from utils.text_predict import predict_text
from utils.image_predict import predict_image
from utils.voice_predict import predict_voice

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/text")
def text_page():
    return render_template("text.html")


@app.route("/image")
def image_page():
    return render_template("image.html")


@app.route("/voice")
def voice_page():
    return render_template("voice.html")


# =========================
# TEXT DETECTION
# =========================
@app.route("/predict_text", methods=["POST"])
def text_detection():
    text = request.form.get("text")

    if not text:
        return "No text provided"

    prediction, confidence = predict_text(text)

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=round(confidence, 2)
    )


# =========================
# IMAGE DETECTION
# =========================
@app.route("/predict_image", methods=["POST"])
def image_detection():
    file = request.files.get("image")

    if not file or file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    prediction, confidence = predict_image(filepath)

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=round(confidence * 100, 2),
        image=file.filename
    )


# =========================
# VOICE DETECTION
# =========================
@app.route("/predict_voice", methods=["POST"])
def voice_detection():
    file = request.files.get("audio")

    if not file or file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    prediction, confidence = predict_voice(filepath)

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=confidence
    )


# =========================
# MAIN (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)