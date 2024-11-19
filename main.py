import logging
from auth import auth_test
from api_intercom import fetch_all_conversations
from save_file import save_to_csv
from data_processing import enrich_contacts_with_client_data

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
        data_processed = enrich_contacts_with_client_data(conversations)

        save_to_csv(data_processed)

        logging.info("Processo concluído.")
