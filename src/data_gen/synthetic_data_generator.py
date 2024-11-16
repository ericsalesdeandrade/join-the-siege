import os
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import random

# Initialize Faker for random data generation
faker = Faker()

# Font setup
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"  # Update if necessary
FONT_SIZE = 14

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
except OSError:
    print("Custom font not found. Using default font.")
    font = ImageFont.load_default()

# General configurations
TEMPLATE_SIZE = (800, 600)  # Width x Height for invoices and bank statements
BACKGROUND_COLOR = (255, 255, 255)  # White
TEXT_COLOR = (0, 0, 0)  # Black


def generate_unique_filename(output_dir, base_name, extension):
    """
    Generates a unique filename by appending a random number.
    """
    random_number = random.randint(1000, 9999)
    return os.path.join(output_dir, f"{base_name}_{random_number}.{extension}")


def generate_random_transactions(count=10):
    """
    Generate a list of random transactions for bank statements.
    """
    transactions = []
    for _ in range(count):
        date = faker.date_between(start_date="-1y", end_date="today").strftime("%m/%d/%Y")
        description = random.choice(["Direct Deposit", "POS Purchase", "ATM Withdrawal", "Loan Repayment", "Online Transfer"])
        debit = f"${random.uniform(10, 1000):.2f}" if random.choice([True, False]) else ""
        credit = f"${random.uniform(10, 1000):.2f}" if not debit else ""
        transactions.append((date, description, debit, credit))
    return transactions


def generate_random_invoice_items(count=5):
    """
    Generate a list of random invoice items.
    """
    items = []
    for _ in range(count):
        description = random.choice(["Laptop", "Monitor", "Keyboard", "Mouse", "Desk Chair", "External Hard Drive", "Headphones", "Webcam"])
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(50, 500), 2)
        total_price = round(quantity * unit_price, 2)
        items.append((description, quantity, unit_price, total_price))
    return items


def generate_synthetic_bank_statements(output_dir, count=10):
    os.makedirs(output_dir, exist_ok=True)
    for _ in range(count):
        image = Image.new("RGB", TEMPLATE_SIZE, color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)

        bank_name = f"Bank of {faker.city()}"
        account_holder = faker.name()
        account_number = f"XXXX-XXXX-XXXX-{random.randint(1000, 9999)}"
        statement_period = f"{faker.date_this_year().strftime('%m/%Y')}"
        transactions = generate_random_transactions(count=random.randint(5, 15))

        draw.text((20, 20), bank_name, fill=TEXT_COLOR, font=font)
        draw.text((20, 50), f"Account Holder: {account_holder}", fill=TEXT_COLOR, font=font)
        draw.text((20, 80), f"Account Number: {account_number}", fill=TEXT_COLOR, font=font)
        draw.text((20, 110), f"Statement Period: {statement_period}", fill=TEXT_COLOR, font=font)
        draw.text((20, 150), "Date | Description | Debit ($) | Credit ($)", fill=TEXT_COLOR, font=font)

        y_offset = 180
        for date, description, debit, credit in transactions:
            draw.text((20, y_offset), f"{date} | {description} | {debit} | {credit}", fill=TEXT_COLOR, font=font)
            y_offset += 20

        pdf_file_path = generate_unique_filename(output_dir, "bank_statement", "pdf")
        image.save(pdf_file_path, format="PDF")
        print(f"Saved: {pdf_file_path}")


def generate_synthetic_driver_licenses(output_dir, count=10):
    os.makedirs(output_dir, exist_ok=True)
    for _ in range(count):
        image = Image.new("RGB", (640, 400), color=(240, 240, 240))
        draw = ImageDraw.Draw(image)

        name = faker.name()
        license_number = f"D-{faker.random_int(min=1000, max=9999)}-{faker.random_int(min=1000, max=9999)}"
        dob = faker.date_of_birth().strftime("%m/%d/%Y")
        address = faker.address().replace("\n", ", ")
        expiration_date = faker.date_this_decade(after_today=True).strftime("%m/%d/%Y")

        draw.text((20, 20), "DRIVER'S LICENSE", fill=TEXT_COLOR, font=font)
        draw.text((20, 60), f"Name: {name}", fill=TEXT_COLOR, font=font)
        draw.text((20, 100), f"License No: {license_number}", fill=TEXT_COLOR, font=font)
        draw.text((20, 140), f"DOB: {dob}", fill=TEXT_COLOR, font=font)
        draw.text((20, 180), f"Address: {address}", fill=TEXT_COLOR, font=font)
        draw.text((20, 220), f"Expires: {expiration_date}", fill=TEXT_COLOR, font=font)
        draw.rectangle([(500, 50), (600, 150)], outline=TEXT_COLOR, width=2)
        draw.text((510, 80), "PHOTO", fill=TEXT_COLOR, font=font)

        file_path = generate_unique_filename(output_dir, "license", "jpg")
        image.save(file_path)
        print(f"Saved: {file_path}")


def generate_synthetic_invoices(output_dir, count=10):
    os.makedirs(output_dir, exist_ok=True)
    for _ in range(count):
        image = Image.new("RGB", TEMPLATE_SIZE, color=BACKGROUND_COLOR)
        draw = ImageDraw.Draw(image)

        invoice_number = f"INV-{random.randint(1000, 9999)}"
        invoice_date = faker.date_between(start_date="-1y", end_date="today").strftime("%m/%d/%Y")
        company_name = f"{faker.company()}"
        customer_name = faker.name()
        customer_address = faker.address().replace("\n", ", ")
        items = generate_random_invoice_items(count=random.randint(3, 7))

        draw.text((20, 20), "INVOICE", fill=TEXT_COLOR, font=font)
        draw.text((20, 50), f"Invoice Number: {invoice_number}", fill=TEXT_COLOR, font=font)
        draw.text((20, 80), f"Date: {invoice_date}", fill=TEXT_COLOR, font=font)
        draw.text((20, 110), f"Company: {company_name}", fill=TEXT_COLOR, font=font)
        draw.text((20, 140), f"Customer: {customer_name}", fill=TEXT_COLOR, font=font)
        draw.text((20, 170), f"Address: {customer_address}", fill=TEXT_COLOR, font=font)

        y_offset = 250
        total_amount = 0
        for description, quantity, unit_price, total_price in items:
            draw.text((20, y_offset), f"{description} | {quantity} | ${unit_price:.2f} | ${total_price:.2f}", fill=TEXT_COLOR, font=font)
            total_amount += total_price
            y_offset += 20

        draw.text((400, y_offset), "Total Amount:", fill=TEXT_COLOR, font=font)
        draw.text((550, y_offset), f"${total_amount:.2f}", fill=TEXT_COLOR, font=font)

        pdf_file_path = generate_unique_filename(output_dir, "invoice", "pdf")
        image.save(pdf_file_path, format="PDF")
        print(f"Saved: {pdf_file_path}")


if __name__ == "__main__":
    generate_synthetic_bank_statements("./training_data/bank_statements/", count=1)
    # generate_synthetic_driver_licenses("./training_data/driver_licenses/", count=10)
    # generate_synthetic_invoices("./training_data/invoices/", count=10)
