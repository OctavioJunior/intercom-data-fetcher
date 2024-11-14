import os
import logging
import pandas as pd


def save_to_csv(conversations, file_name="conversas_intercom.csv"):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    logging.info(f"Convertendo dados para CSV")

    df = pd.DataFrame(conversations)
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path}")
