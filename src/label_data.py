import os
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from src.file_io import extract_text_with_fallback, preprocess_text, allowed_file

def process_file(file_path, label):
    """
    Processes a single file and returns a tuple of (clean_text, label).
    """
    try:
        # Ensure the file is allowed
        if not allowed_file(file_path):
            print(f"Unsupported file format for {file_path}. Skipping.")
            return None

        # Extract and preprocess text
        raw_text = extract_text_with_fallback(file_path)
        clean_text = preprocess_text(raw_text)
        return (clean_text, label)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None


def create_dataset(data_folder):
    """
    Creates a dataset of (text, label) pairs using parallel processing.
    """
    dataset = []
    tasks = []

    with ProcessPoolExecutor() as executor:
        for label in os.listdir(data_folder):  # Iterate over label folders
            label_path = os.path.join(data_folder, label)
            if os.path.isdir(label_path):
                for file_name in os.listdir(label_path):  # Iterate over files in the folder
                    file_path = os.path.join(label_path, file_name)
                    tasks.append(executor.submit(process_file, file_path, label))

        for task in tasks:
            result = task.result()
            if result:
                dataset.append(result)

    return dataset


def save_dataset_to_json(dataset, output_file):
    """
    Saves the dataset to a JSON file.
    """
    try:
        with open(output_file, "w") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving dataset to {output_file}: {e}")


def dataset_statistics(dataset):
    """
    Computes statistics about the dataset.
    """
    labels = [label for _, label in dataset]
    return dict(Counter(labels))


if __name__ == "__main__":
    data_folder = "./training_data"
    output_file = "dataset.json"

    print("Creating dataset...")
    dataset = create_dataset(data_folder)

    print("Saving dataset to JSON...")
    save_dataset_to_json(dataset, output_file)

    print("Dataset created successfully!")
    print("Dataset statistics:")
    print(dataset_statistics(dataset))
