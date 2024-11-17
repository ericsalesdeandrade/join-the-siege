import os
import json
import re
import logging
import joblib
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, "train_model.log"))
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

def load_dataset(file_path):
    """
    Loads the dataset from a JSON file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        logger.info(f"Dataset loaded successfully from {file_path}.")
        return data
    except Exception as e:
        logger.error(f"Error loading dataset from {file_path}: {e}", exc_info=True)
        raise


def preprocess_text(text):
    """
    Preprocess the input text by removing extra spaces.
    """
    try:
        text = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception as e:
        logger.error(f"Error preprocessing text: {text}. Exception: {e}", exc_info=True)
        raise


def split_dataset(texts, labels):
    """
    Splits the dataset into training, validation, and test sets.
    """
    try:
        X_train, X_temp, y_train, y_temp = train_test_split(
            texts, labels, test_size=0.2, stratify=labels, random_state=42
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
        )
        logger.info("Dataset split into training, validation, and test sets.")
        return X_train, X_val, X_test, y_train, y_val, y_test
    except Exception as e:
        logger.error("Error splitting the dataset.", exc_info=True)
        raise


def train_classifier(X_train, y_train):
    """
    Trains a logistic regression classifier and returns the model.
    """
    try:
        model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
        model.fit(X_train, y_train)
        logger.info("Classifier trained successfully.")
        return model
    except Exception as e:
        logger.error("Error training the classifier.", exc_info=True)
        raise


def evaluate_model(model, X, y, dataset_name):
    """
    Evaluates the model on a given dataset and prints the classification report.
    """
    try:
        y_pred = model.predict(X)
        logger.info(f"\n{dataset_name} Set Results:\n{classification_report(y, y_pred)}")
    except Exception as e:
        logger.error(f"Error evaluating the model on {dataset_name} set.", exc_info=True)
        raise


if __name__ == '__main__':
    try:
        dataset_path = "dataset.json"
        dataset = load_dataset(dataset_path)
        texts = [preprocess_text(text) for text, label in dataset]
        labels = [label for _, label in dataset]

        class_distribution = Counter(labels)
        logger.info(f"Class Distribution: {class_distribution}")

        X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(texts, labels)

        vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 4), stop_words=None)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_val_tfidf = vectorizer.transform(X_val)
        X_test_tfidf = vectorizer.transform(X_test)
        logger.info("TF-IDF feature extraction completed.")

        model = train_classifier(X_train_tfidf, y_train)

        joblib.dump(model, "./src/models/text_classifier.pkl")
        joblib.dump(vectorizer, "./src/models/tfidf_vectorizer.pkl")
        logger.info("Model and vectorizer saved successfully.")

        evaluate_model(model, X_val_tfidf, y_val, "Validation")
        evaluate_model(model, X_test_tfidf, y_test, "Test")

        logger.info("\nTesting Classifier on New Inputs\n" + "-" * 40)
        test_cases = [
            "Invoice Number: 12345 for electronics purchase, total $500.",
            "Account Statement: Savings Account XXXX-1234. Balance: $10,000.",
            "Driver's License: Name: John Doe, License No: D12345678.",
        ]
        for i, text in enumerate(test_cases, start=1):
            preprocessed_text = preprocess_text(text)
            new_text_tfidf = vectorizer.transform([preprocessed_text])
            probabilities = model.predict_proba(new_text_tfidf)[0]
            predicted_label = model.classes_[probabilities.argmax()]
            logger.info(f"Test Case {i}: {text}")
            logger.info(f"Predicted Category: {predicted_label}")
            for label, prob in zip(model.classes_, probabilities):
                logger.info(f"  {label}: {prob:.2f}")
            logger.info("-" * 40)

    except Exception as e:
        logger.error("An error occurred during training.", exc_info=True)
