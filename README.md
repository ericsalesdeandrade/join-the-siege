# Document Classifier Project

## 1. **Brief Overview**

This project is a document classification system designed to identify and categorize documents into pre-defined categories. The classifier supports **Invoices**, **Bank Statements**, and **Driver's Licenses**. It leverages a basic Logistic Regression machine learning model and a Flask-based REST API to handle file uploads, extract text, and classify documents.

### **Architecture**

-   **Flask API**: Provides endpoints to classify uploaded files.
-   **Text Extraction**: Uses PyMuPDF, Tesseract OCR, and other libraries to extract text from PDFs, images, DOCX, and XLSX files.
-   **Classification Model**: A Logistic Regression model trained with TF-IDF features.
-   **Logging**: Implements structured logging for debugging and auditing purposes.
-   **File Types Supported**:
    -   PDFs (`.pdf`)
    -   Images (`.jpg`, `.png`)
    -   Word Documents (`.docx`)
    -   Excel Spreadsheets (`.xlsx`)

## 2. How to Run the Flask App
**Prerequisites**
1. Install Python 3.9+ (this project was developed with Python 3.12.3)

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `Terract OCR` is installed on your system.
   - Ubuntu:
    ```bash
      sudo apt-get install tesseract-ocr
    ```
    - MacOS:
    ```bash
    brew install tesseract
    ```

    - Windows:
    - Download the installer from the [official website](https://github.com/UB-Mannheim/tesseract/wiki)

3. Run the Flask app:
   1. Start the Flask server:
   ```bash
   python -m src.app
   ```

   2. Access the API at
    ```bash
    http://127.0.0.1:5000/classify_file
    ```

## 3. Sample API Request and Response
**API Endpoint**
- POST /classify_file

**Headers**
- Content-Type: multipart/form-data

**Request Body**
- file: (file) The file to classify

```bash
curl -X POST http://127.0.0.1:5000/classify_file \
-F "file=@./examples/sample_invoice.pdf"
```

**Response**
```json
{
  "file_class": "invoices"
}
```

## How to Run the Tests
1. Run the tests:
   ```bash
   pytest
   ```

2. Run Unit Tests:
   ```bash
   pytest tests/unit
   ```
3. Run E2E Tests:
   ```bash
    pytest tests/e2e
    ```
4. Run Tests with markers:
   ```
    pytest -m slow
    pytest -m fast
    ``` 

## 5. How to Run CI (GitHub Actions)
This project uses GitHub Actions for Continuous Integration. 

The CI pipeline runs the following steps:

1. Install dependencies.
2. Run tests using pytest.

**Triggering CI**
CI is triggered automatically on every push or pull request to the repository.


**Project Logs**
Logs are saved in the `logs/` directory:

`app.log`: Logs related to Flask API.
`classifier.log`: Logs for the document classification process.
`file_io.log`: Logs for text extraction.


## Limitations & Areas for Improvement

While the project demonstrates a functional document classification pipeline, there are several limitations and areas for potential enhancement:

### **1. Model Training**
- **Synthetic Data**: The model is trained predominantly on synthetic data, which may not reflect real-world document diversity. This could lead to poor performance on actual data due to the lack of variability in text patterns, layouts, and noise.
- **Recommended Actions**:
  - Train the model on a dataset containing **real-world examples** of invoices, bank statements, driver's licenses and various other types of documents in different formats beyond `.pdf`, `.docx`, `.jpg/png` and `xlsx`.
  - Ensure a diverse dataset to minimize bias and account for various formats, languages, and noise levels.
  - Evaluate the model for **bias and overfitting** by examining metrics like the confusion matrix and precision/recall for each class.
  - Use **feature importance** analysis to determine whether critical document elements (e.g., headers, specific keywords) are being captured effectively.
  - Explore **pre-trained models** or **Large Language Models (LLMs)** (e.g., GPT, Llama) for feature extraction and classification to improve performance.
  - Test on documents from various industries and regions to ensure the model's generalizability.

---

### **2. File Handling**
- **Unvalidated Performance**: The API and text extraction modules have not been tested for handling **large files** (e.g., PDFs with hundreds of pages or complex Excel sheets). Memory and performance bottlenecks might occur.
- **Recommended Actions**:
  - Implement file size limits for the API to avoid server crashes.
  - Optimize text extraction methods to process large files efficiently by:
    - Streaming file content.
    - Limiting the number of pages or rows processed.
    - Using parallelized text extraction.
    - Also include Mime type validation for the uploaded files to ensure that only the supported file types are processed.

---

### **3. Payload Validation**
- **Lack of Strict Validation**: The API does not validate the structure of incoming requests beyond checking file types.
- **Recommended Actions**:
  - Use libraries like **Pydantic** to enforce strict input validation and ensure robust payload handling.
  - Define and validate schemas for uploaded files, including expected formats, sizes, and metadata.

---

### **4. Insufficient Test Coverage**
- **Happy Path Focus**: Current tests primarily cover successful cases (e.g., correctly formatted files).
- **Recommended Actions**:
  - Write **additional unit tests** to cover edge cases and failure scenarios, such as:
    - Unsupported file formats.
    - Corrupted or empty files.
    - Files with noise, overlapping text, or unusual layouts.
  - Include integration and end-to-end tests to validate the pipeline holistically.
  - Ensure tests include **large-scale inputs** and unusual document formats.

---

### **5. Database for Metadata**
- **Missing Database Integration**: The project does not store metadata or logs in a database for auditing, tracking, or analysis.
- **Recommended Actions**:
  - Integrate a **database** (e.g., SQLite, PostgreSQL) to store:
    - Uploaded file metadata (e.g., name, size, type).
    - Classification results.
    - Logs for auditing and debugging.
  - Use an ORM (Object-Relational Mapping) library like **SQLAlchemy** to interact with the database.

## **Appendix**

This appendix provides a step-by-step guide on labeling data, training the classification model, and generating synthetic data for this project.

---

### **1. Labeling Data for Classification**

The `label_data.py` script is used to label and preprocess files for training the classifier. It processes files in a directory structure where each subdirectory corresponds to a class label.

#### **Steps to Label Data**
1. **Organize Files**:
   - Create a directory structure like the following:
     ```
     training_data/
     ├── bank_statements/
     │   ├── file1.pdf
     │   ├── file2.jpg
     ├── invoices/
     │   ├── file3.pdf
     │   ├── file4.png
     ├── drivers_licenses/
         ├── file5.pdf
         ├── file6.jpg
     ```
   - Each subdirectory name (e.g., `bank_statements`, `invoices`, `drivers_licenses`) is treated as the label for the files it contains.

2. **Run the Script**:
   - Use the `label_data.py` script to process and label the data:
     ```bash
     python src/label_data.py
     ```
   - By default, the script will:
     - Extract text from files using the `file_io` module.
     - Preprocess the text for training.
     - Save the labeled dataset to a file named `dataset.json`.

3. **Verify the Dataset**:
   - The output dataset will look like this:
     ```json
     [
       ["Sample text from bank statement file", "bank_statements"],
       ["Sample text from invoice file", "invoices"],
       ["Sample text from driver's license file", "drivers_licenses"]
     ]
     ```

---

### **2. Training the Model**

The `train_model.py` script is used to train the document classifier.

#### **Steps to Train the Model**
1. **Prepare the Dataset**:
   - Ensure `dataset.json` is present in the root directory. This file is generated by the `label_data.py` script.

2. **Run the Training Script**:
   - Use the following command to train the model:
     ```bash
     python src/train_model.py
     ```
   - The script will:
     - Load and preprocess the dataset.
     - Split the data into training, validation, and test sets.
     - Train a `LogisticRegression` model using TF-IDF features.
     - Save the trained model and vectorizer to the `./src/models/` directory.

3. **Check the Training Results**:
   - The script outputs metrics such as precision, recall, and F1-score for the validation and test sets.
   - Example output:
     ```
     Validation Set Results:
                       precision    recall  f1-score   support
     bank_statements       0.98      1.00      0.99       102
     drivers_licenses      1.00      1.00      1.00        95
             invoices      0.97      0.98      0.98       104
     
     Test Set Results:
                       precision    recall  f1-score   support
     bank_statements       0.99      1.00      0.99       103
     drivers_licenses      1.00      0.99      0.99        95
             invoices      0.98      0.97      0.98       103
     ```

---

### **3. Generating Synthetic Data**

The project provides scripts to generate synthetic data for training and testing purposes.

#### **Synthetic Data Generators**
1. **Invoices**:
   - Use the `synthetic_invoices.py` script:
     ```bash
     python src/data_gen/synthetic_invoices.py
     ```
   - This script generates synthetic invoices in PDF, DOCX, and XLSX formats. Adjust the `count` parameter to generate the desired number of files.

2. **Bank Statements**:
   - Use the `synthetic_bank_statements.py` script:
     ```bash
     python src/data_gen/synthetic_bank_statements.py
     ```
   - This script generates synthetic bank statements in PDF, DOCX, and XLSX formats.

3. **Driver's Licenses**:
   - Use the `synthetic_drivers_licenses.py` script:
     ```bash
     python src/data_gen/synthetic_drivers_licenses.py
     ```
   - This script generates driver's licenses in JPG format with random details such as name, address, and license number.

---

Thank you! 🚀
