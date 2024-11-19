import logging
import pandas as pd
import os


def save_to_csv(conversations, file_name="conversas_intercom.csv"):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    logging.info("Preparando dados para o CSV...")
    for conversation in conversations:

        for key, value in conversation.items():
            if isinstance(value, (dict, list)):
                conversation[key] = str(value)

    df = pd.DataFrame(conversations)
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path}")
