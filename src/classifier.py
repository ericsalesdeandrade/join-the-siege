import os
from src.file_io import extract_text_with_fallback, preprocess_text


def classify_document(file, model, vectorizer):
    temp_path = f"/tmp/{file.filename}"
    try:
        file.save(temp_path)
        text = extract_text_with_fallback(temp_path)
        # preprocessed_text = preprocess_text(text)
        text_tfidf = vectorizer.transform([text])
        probabilities = model.predict_proba(text_tfidf)[0]
        probabilities_results = dict(zip(model.classes_, probabilities))
        predicted_label = model.classes_[probabilities.argmax()]
        print(f"Predicted Label: {predicted_label}")
        print("Class Probabilities:")
        for label, prob in probabilities_results.items():
            print(f"  {label}: {prob:.2f}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return predicted_label

