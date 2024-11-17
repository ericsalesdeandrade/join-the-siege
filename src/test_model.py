import joblib
from train_model import preprocess_text

model = joblib.load("./src/models/text_classifier.pkl")
vectorizer = joblib.load("./src/models/tfidf_vectorizer.pkl")

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
        "text": "Account Holder: Eric Sales De Andrade Account Number: XXXX-XXXX-XXXX-3452 Statement Period: 12/2024 Date | Description | Debit ($) | Credit ($) 03/11/2024 | Direct Deposit | 836.54 | 07/11/2024 | Bank Fee | 769.98 | 02/11/2024 | Bank Fee | 770.81 | 15/11/2024 | ATM Withdrawal | 512.49 | 727.2 15/11/2024 | Direct Deposit | 735.19 | 821.96 09/11/2024 | Direct Deposit | 342.94 | 775.6 03/11/2024 | Wire Transfer | 762.79 | 309.95 03/11/2024 | ACH Payment | 323.09 | 532.34",
        "description": "Bank statement-like text"
    }
]

print("Testing Classifier on New Inputs\n" + "-" * 40)
for i, case in enumerate(test_cases, start=1):
    text = case["text"]
    description = case["description"]

    preprocessed_text = preprocess_text(text)
    new_text_tfidf = vectorizer.transform([preprocessed_text])
    probabilities = model.predict_proba(new_text_tfidf)[0]
    predicted_label = model.classes_[probabilities.argmax()]

    print(f"Test Case {i}: {description}")
    print(f"Predicted Category: {predicted_label}")
    print("Probabilities:")
    for label, prob in zip(model.classes_, probabilities):
        print(f"  {label}: {prob:.2f}")
    print("-" * 40)
