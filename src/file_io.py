import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_with_fallback(file_path):
    """
    Extracts text from a file using PyMuPDF or Tesseract for images.
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
        print(f"Error extracting text: {e}")
        return ""

def preprocess_text(text):
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()