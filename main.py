import logging
from auth import auth_test
from api_intercom import fetch_all_conversations
from data_processing import process_conversations
from save_file import save_to_csv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    logging.info("Iniciando o processo de busca de conversas no Intercom.")

    if not auth_test():
        logging.error("Autenticação falhou. O processo será interrompido.")
    else:
        start_date = "2024-01-01"
        end_date = "2024-01-01"

        conversations = fetch_all_conversations(start_date, end_date)

        processed_data = process_conversations(conversations)

        save_to_csv(processed_data)

        logging.info("Processo concluído.")
