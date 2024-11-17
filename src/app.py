from flask import Flask, request, jsonify
import joblib
from src.classifier import classify_document
from src.file_io import allowed_file

app = Flask(__name__)

print("Loading model and vectorizer...")
model = joblib.load("./src/models/text_classifier.pkl")
vectorizer = joblib.load("./src/models/tfidf_vectorizer.pkl")
print("Model and vectorizer loaded successfully.")

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    file_class = classify_document(file, model, vectorizer)
    return jsonify({"file_class": file_class}), 200


if __name__ == '__main__':
    app.run(debug=True)
