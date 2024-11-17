import os
from io import BytesIO
import pytest

@pytest.mark.slow
def test_no_file_in_request(client):
    """
    Test if the API returns 400 when no file is in the request.
    """
    response = client.post('/classify_file')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No file part in the request"}

@pytest.mark.slow
def test_no_selected_file(client):
    """
    Test if the API returns 400 when no file is selected.
    """
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json() == {"error": "No selected file"}

@pytest.mark.slow
def test_file_type_not_allowed(client):
    """
    Test if the API returns 400 when the uploaded file type is not allowed.
    """
    data = {'file': (BytesIO(b"dummy content"), 'file.txt')}
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.get_json() == {"error": "File type not allowed"}

@pytest.mark.slow
def test_successful_classification(client):
    """
    Test the /classify_file endpoint using real test files from the ./files directory.
    """
    # Directory containing test files
    test_dir = "./test_data/"

    expected_results = {
        "invoice_1.pdf": "invoices",
        "invoice_2.pdf": "invoices",
        "invoice_3.pdf": "invoices",
        "invoice_499.pdf": "invoices",
        "bank_statement_1.pdf": "bank_statements",
        "bank_statement_2.pdf": "bank_statements",
        "bank_statement_3.pdf": "bank_statements",
        "bank_statement_2500.pdf": "bank_statements",
        "drivers_license_1.jpg": "drivers_licenses",
        "drivers_licence_2.jpg": "drivers_licenses",
        "drivers_license_3.jpg": "drivers_licenses",
        "sample_dl.png": "drivers_licenses",
    }

    for filename, expected_class in expected_results.items():
        file_path = os.path.join(test_dir, filename)
        with open(file_path, "rb") as file_data:
            data = {'file': (BytesIO(file_data.read()), filename)}
            response = client.post('/classify_file', data=data, content_type='multipart/form-data')

        # Assertions
        assert response.status_code == 200
        assert response.get_json() == {"file_class": expected_class}, f"Failed for {filename}"
