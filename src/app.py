import os
import logging
from flask import Flask, request, jsonify
import joblib
from src.classifier import classify_document
from src.file_io import allowed_file

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

flask_logger = logging.getLogger("werkzeug")  
flask_logger.setLevel(logging.DEBUG)
flask_logger.addHandler(file_handler)


app = Flask(__name__)

try:
    logger.info("Loading model and vectorizer...")
    model = joblib.load("./src/models/text_classifier.pkl")
    vectorizer = joblib.load("./src/models/tfidf_vectorizer.pkl")
    logger.info("Model and vectorizer loaded successfully.")
except Exception as e:
    logger.error("Error loading model or vectorizer", exc_info=True)
    raise

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    """
    Route to classify an uploaded file.

    Returns:
        JSON response with the predicted class or error message.
    """
    try:
        if 'file' not in request.files:
            logger.warning("No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            logger.warning("No selected file")
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            logger.warning(f"File type not allowed: {file.filename}")
            return jsonify({"error": "File type not allowed"}), 400

        logger.info(f"Classifying file: {file.filename}")
        file_class = classify_document(file, model, vectorizer)
        logger.info(f"Classification result: {file_class}")

        return jsonify({"file_class": file_class}), 200

    except Exception as e:
        logger.error("Error during file classification", exc_info=True)
        return jsonify({"error": "An error occurred during classification"}), 500

if __name__ == '__main__':
    app.run(debug=True)
