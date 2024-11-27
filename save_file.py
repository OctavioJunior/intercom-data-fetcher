import logging
import pandas as pd
import os
from logging_config import get_folder_path


def prepare_file_paths(file_name_prefix, file_name, json_file_name):

    folder_path = get_folder_path()
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{file_name_prefix}_{file_name}"
    json_file_name = f"{file_name_prefix}_{json_file_name}"

    return os.path.join(folder_path, file_name), os.path.join(
        folder_path, json_file_name
    )


def format_conversations(conversations):

    for conversation in conversations:
        for key, value in conversation.items():
            if isinstance(value, (dict, list)):
                conversation[key] = str(value)
    return conversations


def save_to_csv(
    conversations,
    file_name_prefix="",
    file_name="conversations.csv",
    json_file_name="conversations.json",
):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    logging.info("Preparando dados para o CSV...")

    file_path_csv, file_path_json = prepare_file_paths(
        file_name_prefix, file_name, json_file_name
    )

    formatted_conversations = format_conversations(conversations)

    df = pd.DataFrame(formatted_conversations)

    df.to_csv(file_path_csv, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path_csv}")

    df.to_json(file_path_json, orient="records", lines=True)
    logging.info(f"Arquivo JSON salvo em: {file_path_json}")

    return file_path_csv, file_name
