import fitz
import pandas as pd
import pytest
from docx import Document
from PIL import Image, ImageDraw


@pytest.fixture
def temp_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    with fitz.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), "Sample Text")  # Insert some text
        pdf.save(pdf_path)
    return pdf_path


@pytest.fixture
def temp_image(tmp_path):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", (400, 200), color="white")
    draw = ImageDraw.Draw(image)

    draw.text((50, 50), "Hello World", fill="black", spacing=10)
    image.save(image_path)
    return image_path


@pytest.fixture
def temp_docx(tmp_path):
    docx_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("This is a test document.")
    doc.save(docx_path)
    return docx_path


@pytest.fixture
def temp_excel(tmp_path):
    excel_path = tmp_path / "test.xlsx"
    df = pd.DataFrame({"A": [1, 2], "B": ["Text1", "Text2"]})
    df.to_excel(excel_path, index=False)
    return excel_path
