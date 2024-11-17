import logging
import os
import re

import fitz  # PyMuPDF
import pandas as pd
import pytesseract
from docx import Document
from PIL import Image

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, "file_io.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(console_handler)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "docx", "xlsx"}


def allowed_file(filename):
    """
    Checks if a file has an allowed extension.
    """
    result = (
        "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )
    logger.debug(f"Allowed file check for {filename}: {result}")
    return result


def extract_text_with_fallback(file_path):
    """
    Extracts text from a file, handling PDFs, images, Word, and Excel files.
    """
    file_path = str(file_path)
    file_extension = file_path.rsplit(".", 1)[-1].lower()
    logger.info(f"Extracting text from file: {file_path} (Extension: {file_extension})")

    try:
        if file_extension == "pdf":
            return extract_text_from_pdf(file_path)
        elif file_extension in {"png", "jpg"}:
            return extract_text_from_image(file_path)
        elif file_extension == "docx":
            return extract_text_from_docx(file_path)
        elif file_extension == "xlsx":
            return extract_text_from_excel(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
    except Exception as e:
        logger.error(
            f"Error during text extraction for {file_path}: {e}", exc_info=True
        )
        return ""


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using PyMuPDF, falling back to OCR if necessary.
    """
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
                else:
                    logger.warning(
                        f"Page text empty for file {file_path}, attempting OCR."
                    )
                    pix = page.get_pixmap()
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(image, config="--psm 6")
        logger.info(f"Text successfully extracted from PDF: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}", exc_info=True)
        return ""


def extract_text_from_image(file_path):
    """
    Extracts text from an image file using Tesseract OCR.
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, config="--psm 6")
        logger.info(f"Text successfully extracted from image: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(
            f"Error extracting text from image {file_path}: {e}", exc_info=True
        )
        return ""


def extract_text_from_docx(file_path):
    """
    Extracts text from a Word (.docx) file using python-docx.
    """
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logger.info(f"Text successfully extracted from Word document: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(
            f"Error extracting text from Word document {file_path}: {e}", exc_info=True
        )
        return ""


def extract_text_from_excel(file_path):
    """
    Extracts text from an Excel (.xlsx) file using pandas.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=None)
        text = ""
        for sheet_name, sheet_df in df.items():
            text += f"Sheet: {sheet_name}\n"
            text += sheet_df.to_string(index=False, header=True)
            text += "\n\n"
        logger.info(f"Text successfully extracted from Excel file: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(
            f"Error extracting text from Excel file {file_path}: {e}", exc_info=True
        )
        return ""


def preprocess_text(text):
    """
    Preprocess the extracted text.
    """
    try:
        processed_text = re.sub(r"\s+", " ", text)
        logger.debug("Text preprocessing completed.")
        return processed_text.strip()
    except Exception as e:
        logger.error(f"Error during text preprocessing: {e}", exc_info=True)
        return ""
