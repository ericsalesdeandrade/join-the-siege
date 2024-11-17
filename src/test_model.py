import os
import joblib
import logging
from train_model import preprocess_text

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, "test_model.log"))
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

try:
    model_path = "./src/models/text_classifier.pkl"
    vectorizer_path = "./src/models/tfidf_vectorizer.pkl"

    logger.info("Loading model and vectorizer...")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    logger.info("Model and vectorizer loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model or vectorizer: {e}", exc_info=True)
    raise

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
        "text": (
            "Account Holder: Eric Sales De Andrade Account Number: XXXX-XXXX-XXXX-3452 "
            "Statement Period: 12/2024 Date | Description | Debit ($) | Credit ($) "
            "03/11/2024 | Direct Deposit | 836.54 | 07/11/2024 | Bank Fee | 769.98 | "
            "02/11/2024 | Bank Fee | 770.81 | 15/11/2024 | ATM Withdrawal | 512.49 | "
            "727.2 15/11/2024 | Direct Deposit | 735.19 | 821.96 09/11/2024 | Direct Deposit "
            "| 342.94 | 775.6 03/11/2024 | Wire Transfer | 762.79 | 309.95 03/11/2024 | "
            "ACH Payment | 323.09 | 532.34"
        ),
        "description": "Detailed bank statement-like text"
    }
]

logger.info("Testing Classifier on New Inputs\n" + "-" * 40)
for i, case in enumerate(test_cases, start=1):
    try:
        text = case["text"]
        description = case["description"]

        preprocessed_text = preprocess_text(text)
        logger.info(f"Preprocessed Text for Test Case {i}: {preprocessed_text}")

        new_text_tfidf = vectorizer.transform([preprocessed_text])

        probabilities = model.predict_proba(new_text_tfidf)[0]
        predicted_label = model.classes_[probabilities.argmax()]

        logger.info(f"Test Case {i}: {description}")
        logger.info(f"Predicted Category: {predicted_label}")
        for label, prob in zip(model.classes_, probabilities):
            logger.info(f"  {label}: {prob:.2f}")
        logger.info("-" * 40)
    except Exception as e:
        logger.error(f"Error processing Test Case {i}: {e}", exc_info=True)
