import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Supported file extensions
SUPPORTED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]

def is_supported_image(url):
    """
    Checks if the URL points to a supported image format.

    Args:
        url (str): Image URL.

    Returns:
        bool: True if the image format is supported, False otherwise.
    """
    for ext in SUPPORTED_EXTENSIONS:
        if url.lower().endswith(ext):
            return True
    return False


def fetch_image_urls_from_url(page_url):
    """
    Fetch all image URLs from a webpage.

    Args:
        page_url (str): URL of the webpage.

    Returns:
        list: List of image URLs found on the page.
    """
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        image_urls = []

        # Find all <img> tags and extract the "src" attribute
        for img_tag in soup.find_all("img"):
            img_url = img_tag.get("src")
            if img_url:
                # Handle relative URLs
                if not img_url.startswith(("http://", "https://")):
                    img_url = requests.compat.urljoin(page_url, img_url)
                if is_supported_image(img_url):
                    image_urls.append(img_url)

        return image_urls
    except Exception as e:
        print(f"Failed to fetch images from {page_url}: {e}")
        return []


def download_images(image_urls, output_dir):
    """
    Download images from the given URLs and save them to the specified directory.

    Args:
        image_urls (list): List of image URLs.
        output_dir (str): Directory to save the images.
    """
    os.makedirs(output_dir, exist_ok=True)

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))

            # Convert RGBA or WEBP to RGB for saving as JPEG
            if image.mode in ("RGBA", "P"):  # Handle transparency or palette
                image = image.convert("RGB")

            # Save as JPEG
            file_path = os.path.join(output_dir, f"image_{idx+1}.jpg")
            image.save(file_path, format="JPEG")
            print(f"Downloaded and converted: {file_path}")
        except Exception as e:
            print(f"Failed to download or convert image from {url}: {e}")



if __name__ == "__main__":
    # Input the URL of the webpage
    webpage_url = "https://www.businessinsider.com/what-drivers-license-looks-like-in-every-state"
    output_directory = "./downloaded_images"

    # Fetch image URLs
    print(f"Fetching image URLs from {webpage_url}...")
    image_urls = fetch_image_urls_from_url(webpage_url)

    # Download images
    if image_urls:
        print(f"Found {len(image_urls)} images. Downloading...")
        download_images(image_urls, output_directory)
        print("Image download complete!")
    else:
        print("No images found.")
