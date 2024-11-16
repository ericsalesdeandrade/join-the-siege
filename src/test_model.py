import joblib
from train_model import preprocess_text

# Load trained model and vectorizer
model = joblib.load("./src/models/text_classifier.pkl")
vectorizer = joblib.load("./src/models/tfidf_vectorizer.pkl")

# Test cases (old + new combined)
test_cases = [
    {
        "text": "Invoice Number: 12345 for electronics purchase, total $500.",
        "description": "Invoice-like text"
    },
    {
        "text": "Account Statement: Savings Account XXXX-1234. Balance: $10,000.",
        "description": "Bank statement-like text"
    },
    {
        "text": "Driver's License: Name: John Doe, License No: D12345678.",
        "description": "Driver's license-like text"
    },
    {
        "text": "Invoice ID: INV12345 | Payment Due: 10/12/2023 | Amount: $1500 | Status: Paid",
        "description": "Detailed invoice text with multiple fields"
    },
    {
        "text": "Account Statement: Checking Account XXXX-4567 | Last Transaction: $50 on 01/12/2023",
        "description": "Bank statement with recent transaction details"
    },
    {
        "text": "Name: Alice Johnson | Driver's License No: A1234567 | Expiry Date: 2025-01-01",
        "description": "Standard driver's license text"
    },
    {
        "text": "Savings Account XXXX-8901 | Balance: $25,000 | Last Withdrawal: $500 on 11/30/2023.",
        "description": "Bank statement summary with large balance"
    },
    {
        "text": "Driver's License for Robert Lee, License ID: R567890, Issued by Texas DMV, Valid until 2026.",
        "description": "Detailed driver's license text with issuing authority"
    }
]

# Unified testing
print("Testing Classifier on New Inputs\n" + "-" * 40)
for i, case in enumerate(test_cases, start=1):
    text = case["text"]
    description = case["description"]

    # Preprocess and predict
    preprocessed_text = preprocess_text(text)
    new_text_tfidf = vectorizer.transform([preprocessed_text])
    probabilities = model.predict_proba(new_text_tfidf)[0]
    predicted_label = model.classes_[probabilities.argmax()]

    # Display results
    print(f"Test Case {i}: {description}")
    print(f"Predicted Category: {predicted_label}")
    print("Probabilities:")
    for label, prob in zip(model.classes_, probabilities):
        print(f"  {label}: {prob:.2f}")
    print("-" * 40)
