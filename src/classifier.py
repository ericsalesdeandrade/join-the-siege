from pypdf import PdfReader
from PIL import Image
import pytesseract
from werkzeug.datastructures import FileStorage
import magic
import pdfplumber
import re

def detect_file_type(file: FileStorage):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(file.read(2048))  
    file.seek(0)  
    return mime_type


def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def classify_document(file):
    """
    Classifies a document into categories: 'invoice', 'driver_license', or 'bank_statement'.
    """
    # Detect file type
    mime_type = detect_file_type(file)
    if mime_type == "application/pdf":
        text = extract_text_from_pdf(file)
    elif mime_type in ("image/jpeg", "image/jpg", "image/png"):
        text = extract_text_from_image(file)

    # Rule-based classification
    invoice_pattern = re.compile(r"invoice", re.IGNORECASE)
    license_pattern = re.compile(r"\blicen[cs]e\b", re.IGNORECASE)
    bank_statement_pattern = re.compile(r"account number", re.IGNORECASE)
    if invoice_pattern.search(text):
        return "invoice"
    elif license_pattern.search(text):
        return "drivers_license"
    elif bank_statement_pattern.search(text):
        return "bank_statement"
    
    return "unknown"
