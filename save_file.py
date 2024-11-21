import logging
import pandas as pd
import os


def save_to_csv(
    conversations,
    file_name_prefix="",
    file_name="conversations_data.csv",
    json_file_name="conversations_data.json",
):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    logging.info("Preparando dados para o CSV...")

    folder_path = os.path.join(os.getenv("HOME"), "intercom_data_fetcher", "files")
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{file_name_prefix}_{file_name}"
    json_file_name = f"{file_name_prefix}_{json_file_name}"

    file_path_csv = os.path.join(folder_path, file_name)
    file_path_json = os.path.join(folder_path, json_file_name)

    for conversation in conversations:
        for key, value in conversation.items():
            if isinstance(value, (dict, list)):
                conversation[key] = str(value)

    df = pd.DataFrame(conversations)

    # Save to CSV
    df.to_csv(file_path_csv, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path_csv}")

    # Save to JSON
    df.to_json(file_path_json, orient="records", lines=True)
    logging.info(f"Arquivo JSON salvo em: {file_path_json}")
