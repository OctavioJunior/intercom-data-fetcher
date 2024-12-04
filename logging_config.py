import logging
import sys
import os
from platform import system


def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    stdout_handler = logging.StreamHandler(sys.stdout)
    stderr_handler = logging.StreamHandler(sys.stderr)
    file_handler = logging.FileHandler(os.path.join(get_folder_path(), "log.txt"))

    stdout_handler.setLevel(logging.INFO)
    stderr_handler.setLevel(logging.ERROR)
    file_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[stdout_handler, stderr_handler, file_handler],
    )


def get_folder_path():

    if os.name == "nt":
        folder_path = os.path.join("C:\\", "intercom_data_fetcher", "files")
    else:
        folder_path = os.path.join(os.getenv("HOME"), "intercom_data_fetcher", "files")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path
