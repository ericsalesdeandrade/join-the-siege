import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str, level: int = logging.INFO):
    """
    Sets up a logger with both file and console handlers.

    Args:
        name (str): The name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO).
    Returns:
        logging.Logger: Configured logger.
    """
    os.makedirs("./logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File Handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    return logger
