import pytest
# from src.app import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

@pytest.fixture
def test_files():
    return [
        {
            "file_name": "bank_statement_1.pdf",
            "expected_mime_type": "application/pdf",
            "type": "bank_statement"    
        },
        {
            "file_name": "bank_statement_2.pdf",
            "expected_mime_type": "application/pdf",
            "type": "bank_statement"
        },
        {
            "file_name": "bank_statement_3.pdf",
            "expected_mime_type": "application/pdf",
            "type": "bank_statement"
        },
        {
            "file_name": "drivers_license_1.jpg",
            "expected_mime_type": "image/jpeg",
            "type": "drivers_license"
        },
        {
            "file_name": "drivers_licence_2.jpg",
            "expected_mime_type": "image/jpeg",
            "type": "drivers_license"
        },
        {
            "file_name": "drivers_license_3.jpg",
            "expected_mime_type": "image/jpeg",
            "type": "drivers_license"
        },
        {
            "file_name": "invoice_1.pdf",
            "expected_mime_type": "application/pdf",
            "type": "invoice"
        },
        {
            "file_name": "invoice_2.pdf",
            "expected_mime_type": "application/pdf",
            "type": "invoice"
        },
        {
            "file_name": "invoice_3.pdf",
            "expected_mime_type": "application/pdf",
            "type": "invoice"
        }
    ]
        
    