import json
import logging
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from src.file_io import (allowed_file, extract_text_with_fallback,
                         preprocess_text)

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(log_dir, "label_data.log"))
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(console_handler)


def process_file(file_path, label):
    """
    Processes a single file and returns a tuple of (clean_text, label).
    """
    try:
        if not allowed_file(file_path):
            logger.warning(f"Unsupported file format for {file_path}. Skipping.")
            return None

        raw_text = extract_text_with_fallback(file_path)
        clean_text = preprocess_text(raw_text)
        logger.info(f"Successfully processed file: {file_path}")
        return (clean_text, label)
    except Exception:
        logger.error(f"Error processing file {file_path}", exc_info=True)
        return None


def create_dataset(data_folder):
    """
    Creates a dataset of (text, label) pairs using parallel processing.
    """
    dataset = []
    tasks = []

    try:
        with ProcessPoolExecutor() as executor:
            for label in os.listdir(data_folder):
                label_path = os.path.join(data_folder, label)
                if os.path.isdir(label_path):
                    logger.info(f"Processing label: {label}")
                    for file_name in os.listdir(label_path):
                        file_path = os.path.join(label_path, file_name)
                        tasks.append(executor.submit(process_file, file_path, label))

            for task in tasks:
                result = task.result()
                if result:
                    dataset.append(result)

        logger.info("Dataset creation completed.")
        return dataset
    except Exception:
        logger.error("Error during dataset creation", exc_info=True)
        return dataset


def save_dataset_to_json(dataset, output_file):
    """
    Saves the dataset to a JSON file.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
        logger.info(f"Dataset saved to {output_file}")
    except Exception:
        logger.error(f"Error saving dataset to {output_file}", exc_info=True)


def dataset_statistics(dataset):
    """
    Computes statistics about the dataset.
    """
    labels = [label for _, label in dataset]
    stats = dict(Counter(labels))
    logger.info(f"Dataset statistics: {stats}")
    return stats


if __name__ == "__main__":
    data_folder = "./training_data"
    output_file = "dataset.json"

    logger.info("Starting dataset creation...")
    dataset = create_dataset(data_folder)

    logger.info("Saving dataset to JSON...")
    save_dataset_to_json(dataset, output_file)

    logger.info("Dataset created successfully!")
    logger.info("Dataset statistics:")
    dataset_statistics(dataset)
