import pytest
import os
from src.classifier import detect_file_type, extract_text_from_pdf, extract_text_from_image, classify_document

def test_detect_file_type(test_files):
    for test_file in test_files:
        file_name = test_file["file_name"]
        expected_mime_type = test_file["expected_mime_type"]

        file_path = os.path.join("./files", file_name)

        assert os.path.exists(file_path), f"Test file {file_name} does not exist in the directory."

        with open(file_path, "rb") as file:
            detected_mime_type = detect_file_type(file)

        assert detected_mime_type == expected_mime_type, (
            f"MIME type mismatch for {file_name}: "
            f"expected {expected_mime_type}, got {detected_mime_type}"
        )
    
def test_extract_text_from_documents(test_files):
    for test_file in test_files:
        file_name = test_file["file_name"]
        expected_mime_type = test_file["expected_mime_type"]

        file_path = os.path.join("./files", file_name)

        assert os.path.exists(file_path), f"Test file {file_name} does not exist in the directory."

        # Open the file in binary mode and extract text based on MIME type
        with open(file_path, "rb") as file:
            if expected_mime_type == "application/pdf":
                text = extract_text_from_pdf(file)
            elif expected_mime_type.startswith("image/"):
                text = extract_text_from_image(file)
            else:
                pytest.fail(f"Unsupported MIME type {expected_mime_type} for {file_name}")

            assert len(text) > 0, f"Extracted text is empty for {file_name}"


def test_classify_document(test_files):
    for test_file in test_files:
        file_name = test_file["file_name"]
        expected_type = test_file["type"]

        file_path = os.path.join("./files", file_name)

        assert os.path.exists(file_path), f"Test file {file_name} does not exist in the directory."

        with open(file_path, "rb") as file:
            try:
                classified_type = classify_document(file)
            except Exception as e:
                pytest.fail(f"Error while classifying {file_name}: {e}")

        assert classified_type == expected_type, (
            f"Classification mismatch for {file_name}: "
            f"expected {expected_type}, got {classified_type}"
        )
