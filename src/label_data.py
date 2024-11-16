import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import json
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

def extract_text_with_fallback(file_path):
    """
    Extracts text from a PDF using PyMuPDF, falling back to OCR for image-based PDFs.
    """
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                # Attempt to extract text directly
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
                else:  # If no text, extract images for OCR
                    pix = page.get_pixmap()  # Extract image from the page
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with fallback from {file_path}: {e}")
        return ""

def extract_text_from_image(file_path):
    """
    Extracts text from an image file.
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image {file_path}: {e}")
        return ""

def preprocess_text(text):
    """
    Cleans up extracted text by removing noise and standardizing terms.
    """
    text = re.sub(r"\s+", " ", text).strip()
    return text

def process_file(file_path, label):
    """
    Processes a single file and returns a tuple of (clean_text, label).
    """
    try:
        if file_path.endswith(".pdf"):
            text = extract_text_with_fallback(file_path)
        elif file_path.endswith((".jpg", ".png")):
            text = extract_text_from_image(file_path)
        else:
            return None
        clean_text = preprocess_text(text)
        return (clean_text, label)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

def create_dataset(data_folder):
    """
    Creates a dataset of (text, label) pairs using parallel processing.
    """
    dataset = []
    tasks = []
    with ProcessPoolExecutor() as executor:
        for label in os.listdir(data_folder):  # Iterate over folders (labels)
            label_path = os.path.join(data_folder, label)
            if os.path.isdir(label_path):
                for file_name in os.listdir(label_path):  # Iterate over files in the folder
                    file_path = os.path.join(label_path, file_name)
                    tasks.append(executor.submit(process_file, file_path, label))

        for task in tasks:
            result = task.result()
            if result:
                dataset.append(result)
    return dataset

def save_dataset_to_json(dataset, output_file):
    """
    Saves the dataset to a JSON file.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving dataset to {output_file}: {e}")

def dataset_statistics(dataset):
    """
    Computes statistics about the dataset.
    """
    labels = [label for _, label in dataset]
    return dict(Counter(labels))

if __name__ == "__main__":
    data_folder = "./data"
    output_file = "dataset.json"

    # Create the dataset
    dataset = create_dataset(data_folder)

    # Save the dataset
    save_dataset_to_json(dataset, output_file)

    # Print statistics
    print("Dataset created successfully!")
    print("Dataset statistics:")
    print(dataset_statistics(dataset))
