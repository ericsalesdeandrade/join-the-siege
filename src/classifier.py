from src.file_io import extract_text_with_fallback, preprocess_text


def classify_document(file, model, vectorizer):
    """
    Classifies the uploaded file based on its content.
    """
    # Save the file temporarily
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    # Extract and preprocess text
    text = extract_text_with_fallback(temp_path)
    preprocessed_text = preprocess_text(text)

    # Classify
    text_tfidf = vectorizer.transform([preprocessed_text])
    predicted_label = model.predict(text_tfidf)[0]

    return predicted_label
