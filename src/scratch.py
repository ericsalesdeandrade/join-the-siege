import fitz

def is_text_pdf(file_path):
    """
    Determines whether a PDF is a text-based PDF or contains only images.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        bool: True if the PDF contains extractable text, False if it is image-based.
    """
    with fitz.open(file_path) as pdf:
        for page in pdf:
            # Check if the page has extractable text
            text = page.get_text()
            print(text)
            if text.strip():  # If there's any extractable text, it's a text PDF
                return True
    return False  # No extractable text found; likely an image-based PDF


print(is_text_pdf("files/invoice_3.pdf"))  # False