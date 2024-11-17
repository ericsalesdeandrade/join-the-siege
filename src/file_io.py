import fitz  
from PIL import Image
import pytesseract
import re
import os
from docx import Document
import pandas as pd

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'docx', 'xlsx'}

def allowed_file(filename):
    """
    Checks if a file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_with_fallback(file_path):
    """
    Extracts text from a file, handling PDFs, images, Word, and Excel files.
    """
    file_path = str(file_path)  
    file_extension = file_path.rsplit('.', 1)[-1].lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in {'png', 'jpg'}:
        return extract_text_from_image(file_path)
    elif file_extension == 'docx':
        return extract_text_from_docx(file_path)
    elif file_extension == 'xlsx':
        return extract_text_from_excel(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")


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
                    pix = page.get_pixmap()
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def extract_text_from_image(file_path):
    """
    Extracts text from an image file using Tesseract OCR.
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, config="--psm 6")
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def extract_text_from_docx(file_path):
    """
    Extracts text from a Word (.docx) file using python-docx.
    """
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from Word document: {e}")
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
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from Excel file: {e}")
        return ""

def preprocess_text(text):
    """
    Preprocess the extracted text.
    """
    text = re.sub(r"\s+", " ", text)
    return text
