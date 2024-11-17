import os
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import random

faker = Faker()

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf" 
FONT_SIZE = 16
FONT_SIZE_SMALL = 12

try:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    font_small = ImageFont.truetype(FONT_PATH, FONT_SIZE_SMALL)
except OSError:
    print("Custom font not found. Using default font.")
    font = ImageFont.load_default()
    font_small = ImageFont.load_default()

LICENSE_SIZE = (800, 400)
BACKGROUND_COLORS = [(240, 240, 240), (200, 255, 255), (255, 228, 225)]
TEXT_COLOR = (0, 0, 0)
PHOTO_SIZE = (120, 120)


def generate_unique_filename(output_dir, base_name, extension):
    """
    Generates a unique filename by appending a random number.
    """
    random_number = random.randint(1000, 9999)
    return os.path.join(output_dir, f"{base_name}_{random_number}.{extension}")


def generate_synthetic_driver_licenses(output_dir, count=10):
    os.makedirs(output_dir, exist_ok=True)

    for _ in range(count):
        background_color = random.choice(BACKGROUND_COLORS)
        image = Image.new("RGB", LICENSE_SIZE, color=background_color)
        draw = ImageDraw.Draw(image)

        name = faker.name()
        license_number = f"{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"
        dob = faker.date_of_birth().strftime("%m/%d/%Y")
        address = faker.address().replace("\n", ", ")
        expiration_date = faker.date_this_decade(after_today=True).strftime("%m/%d/%Y")
        issue_date = faker.date_this_decade(before_today=True).strftime("%m/%d/%Y")
        height = f"{random.randint(4, 6)}-{random.randint(0, 11)}"
        weight = random.randint(100, 250)
        eyes = random.choice(["Brown", "Blue", "Green", "Hazel"])
        hair = random.choice(["Black", "Brown", "Blonde", "Red", "Gray"])
        sex = random.choice(["M", "F"])
        state = faker.state_abbr()

        draw.text((20, 20), f"{state} DRIVER'S LICENSE", fill=TEXT_COLOR, font=font)

        draw.text((20, 60), f"License No: {license_number}", fill=TEXT_COLOR, font=font)
        draw.text((20, 100), f"Name: {name}", fill=TEXT_COLOR, font=font)
        draw.text((20, 140), f"DOB: {dob}", fill=TEXT_COLOR, font=font)
        draw.text((20, 180), f"Address: {address}", fill=TEXT_COLOR, font=font)
        draw.text((20, 220), f"Expires: {expiration_date}", fill=TEXT_COLOR, font=font)
        draw.text((20, 260), f"Issue Date: {issue_date}", fill=TEXT_COLOR, font=font)
        draw.text((20, 300), f"Height: {height}   Weight: {weight}   Eyes: {eyes}   Hair: {hair}   Sex: {sex}", fill=TEXT_COLOR, font=font_small)

        photo_position = (600, 50)
        photo_box = (photo_position[0], photo_position[1], photo_position[0] + PHOTO_SIZE[0], photo_position[1] + PHOTO_SIZE[1])
        draw.rectangle(photo_box, outline=TEXT_COLOR, width=2)
        draw.text((photo_position[0] + 25, photo_position[1] + 45), "PHOTO", fill=TEXT_COLOR, font=font_small)
        draw.text((600, 250), "ISSUED BY DMV", fill=TEXT_COLOR, font=font_small)
        draw.ellipse([(650, 300), (750, 350)], outline=TEXT_COLOR, width=2)
        draw.text((665, 315), "DMV", fill=TEXT_COLOR, font=font_small)

        draw.rectangle([(10, 10), (790, 390)], outline=(0, 0, 0), width=3)

        file_path = generate_unique_filename(output_dir, "driver_license", "jpg")
        image.save(file_path, format="JPEG")
        print(f"Saved: {file_path}")


if __name__ == "__main__":
    output_base_dir = "./training_data/drivers_licenses/"
    generate_synthetic_driver_licenses(output_base_dir, count=1000)
