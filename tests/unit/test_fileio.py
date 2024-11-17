import pytest
import re
from src.file_io import (
    allowed_file,
    extract_text_with_fallback,
    extract_text_from_pdf,
    extract_text_from_image,
    extract_text_from_docx,
    extract_text_from_excel,
)

@pytest.mark.fast
@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.docx", True),
    ("file.xlsx", True),
    ("file.txt", False),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

@pytest.mark.fast
def test_extract_text_from_pdf(temp_pdf):
    text = extract_text_from_pdf(temp_pdf)
    assert isinstance(text, str)
    assert text == "Sample Text"

@pytest.mark.fast
def test_extract_text_from_image(temp_image):
    text = extract_text_from_image(temp_image)
    assert isinstance(text, str)
    pattern = r"Hello\s*world"
    assert re.search(pattern, text), f"Extracted text '{text}' does not match expected pattern '{pattern}'"

@pytest.mark.fast
def test_extract_text_from_docx(temp_docx):
    text = extract_text_from_docx(temp_docx)
    assert isinstance(text, str)
    assert "This is a test document." in text

@pytest.mark.fast
def test_extract_text_from_excel(temp_excel):
    text = extract_text_from_excel(temp_excel)
    assert isinstance(text, str)
    assert "Text1" in text
    assert "Text2" in text

@pytest.mark.parametrize("fixture", ["temp_pdf", "temp_image", "temp_docx", "temp_excel"])
@pytest.mark.fast
def test_extract_text_with_fallback(fixture, request):
    file_path = request.getfixturevalue(fixture)
    text = extract_text_with_fallback(file_path)
    assert isinstance(text, str)
    assert text != ""  
