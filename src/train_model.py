import json
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from collections import Counter
from nltk.stem import PorterStemmer

# Step 1: Load the dataset
def load_dataset(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Step 2: Preprocess the data
def preprocess_text(text):
    ps = PorterStemmer()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters and numbers
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    words = text.lower().strip().split()
    return " ".join([ps.stem(word) for word in words])

# Load and preprocess data
dataset = load_dataset("dataset.json")
texts = [preprocess_text(text) for text, label in dataset]
labels = [label for text, label in dataset]

# Display class distribution
print("Class Distribution:", Counter(labels))

# Step 3: Split the dataset
X_train, X_temp, y_train, y_temp = train_test_split(
    texts, labels, test_size=0.2, stratify=labels, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

# Step 4: Feature extraction using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english")
X_train_tfidf = vectorizer.fit_transform(X_train)
X_val_tfidf = vectorizer.transform(X_val)
X_test_tfidf = vectorizer.transform(X_test)

# Step 5: Train the classifier
model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
model.fit(X_train_tfidf, y_train)

# Save the model and vectorizer
joblib.dump(model, "text_classifier.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("Model and vectorizer saved as 'text_classifier.pkl' and 'tfidf_vectorizer.pkl'")


if __name__ == '__main__':

    # Example:
    print("\nValidation Set Results:")
    y_val_pred = model.predict(X_val_tfidf)
    print(classification_report(y_val, y_val_pred))

    print("\nTest Set Results:")
    y_test_pred = model.predict(X_test_tfidf)
    print(classification_report(y_test, y_test_pred))

    # Example test cases
    test_cases = [
        "Invoice Number: 12345 for electronics purchase, total $500.",
        "Account Statement: Savings Account XXXX-1234. Balance: $10,000.",
        "Driver's License: Name: John Doe, License No: D12345678.",
    ]
    print("\nTesting Classifier on New Inputs\n" + "-" * 40)
    for i, text in enumerate(test_cases, start=1):
        preprocessed_text = preprocess_text(text)
        new_text_tfidf = vectorizer.transform([preprocessed_text])
        probabilities = model.predict_proba(new_text_tfidf)[0]
        predicted_label = model.classes_[probabilities.argmax()]
        print(f"Test Case {i}: {text}")
        print(f"Predicted Category: {predicted_label}")
        print("Probabilities:")
        for label, prob in zip(model.classes_, probabilities):
            print(f"  {label}: {prob:.2f}")
        print("-" * 40)

