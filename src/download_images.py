import os
import requests
from PIL import Image
from io import BytesIO

# Your SerpAPI key
SERPAPI_API_KEY = ""

# Search parameters for Google Images
SEARCH_QUERY = "driver license sample"
NUM_IMAGES = 100  # Number of images to download
OUTPUT_DIR = "./driver_license_images"


def fetch_image_urls(query, num_images, api_key):
    """
    Fetch image URLs using SerpAPI Google Images API.

    Args:
        query (str): Search query.
        num_images (int): Number of image URLs to fetch.
        api_key (str): SerpAPI API key.

    Returns:
        list: List of image URLs.
    """
    image_urls = []
    page = 0
    while len(image_urls) < num_images:
        # API request URL
        url = "https://serpapi.com/search.json"
        params = {
            "q": query,
            "tbm": "isch",
            "ijn": page,
            "api_key": api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for result in data.get("images_results", []):
            image_urls.append(result["original"])
            if len(image_urls) >= num_images:
                break

        page += 1

    return image_urls[:num_images]


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

            # Convert RGBA images to RGB
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # Save the image
            file_path = os.path.join(output_dir, f"driver_license_{idx+1}.jpg")
            image.save(file_path, format="JPEG")
            print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"Failed to download image from {url}: {e}")


if __name__ == "__main__":
    # Fetch image URLs
    print("Fetching image URLs...")
    image_urls = fetch_image_urls(SEARCH_QUERY, NUM_IMAGES, SERPAPI_API_KEY)

    # Download images
    print("Downloading images...")
    download_images(image_urls, OUTPUT_DIR)

    print("Image download complete!")
