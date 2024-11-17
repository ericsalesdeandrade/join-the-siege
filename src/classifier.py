import os

from src.file_io import extract_text_with_fallback, preprocess_text
from src.logging_config import setup_logger

logger = setup_logger("classifier", "./logs/classifier.log")


def classify_document(file, model, vectorizer):
    """
    Classify a document by extracting its text, preprocessing it, and using the model to predict its class.

    Args:
        file: Uploaded file object.
        model: Trained classification model.
        vectorizer: Pretrained vectorizer for text transformation.

    Returns:
        str: Predicted label of the document.
    """
    temp_path = f"/tmp/{file.filename}"
    try:
        file.save(temp_path)
        logger.info(f"File saved temporarily: {temp_path}")

        text = extract_text_with_fallback(temp_path)
        if not text:
            logger.warning(f"No text extracted from file: {temp_path}")
            return "Unknown"

        preprocessed_text = preprocess_text(text)
        logger.debug(f"Preprocessed text: {preprocessed_text}")

        text_tfidf = vectorizer.transform([preprocessed_text])

        probabilities = model.predict_proba(text_tfidf)[0]
        probabilities_results = dict(zip(model.classes_, probabilities))
        predicted_label = model.classes_[probabilities.argmax()]

        logger.info(f"Predicted Label: {predicted_label}")
        logger.info("Class Probabilities:")
        for label, prob in probabilities_results.items():
            logger.info(f"  {label}: {prob:.2f}")

        return predicted_label

    except Exception as e:
        logger.error(f"Error during document classification: {e}", exc_info=True)
        return "Error"

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Temporary file deleted: {temp_path}")
