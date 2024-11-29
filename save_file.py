import os
import json
import logging
import pandas as pd
from csv_converter import csv_converter
from logging_config import get_folder_path


def prepare_file_paths(file_name_prefix, file_name, json_file_name):
    folder_path = get_folder_path()
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{file_name_prefix}_{file_name}"
    json_file_name = f"{file_name_prefix}_{json_file_name}"

    return os.path.join(folder_path, file_name), os.path.join(
        folder_path, json_file_name
    )


def save_to_csv(
    conversations,
    file_name_prefix="",
    file_name="conversations.csv",
    json_file_name="conversations.json",
):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    logging.info("Preparando dados para salvar...")

    file_path_csv, file_path_json = prepare_file_paths(
        file_name_prefix, file_name, json_file_name
    )

    with open(file_path_json, "w", encoding="utf-8") as json_file:
        json.dump(conversations, json_file, ensure_ascii=False, indent=4)
    logging.info(f"Arquivo JSON original salvo em: {file_path_json}")

    expanded_conversations = csv_converter(conversations)

    df = pd.DataFrame(expanded_conversations)

    df.to_csv(file_path_csv, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path_csv}")

    return file_path_csv, file_name
