import logging
from auth import auth_test
from api_intercom import fetch_all_conversations
from save_file import save_to_csv
from data_processing import enrich_contacts_with_client_data
from datetime import datetime, timedelta

# Configuração de logging (uma única vez)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
)

if __name__ == "__main__":
    logging.info("Iniciando o processo de busca de conversas no Intercom.")

    # Calculando as datas para o dia anterior
    yesterday = datetime.now() - timedelta(1)
    start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    end_date = yesterday.replace(
        hour=23, minute=59, second=59, microsecond=999999
    ).strftime("%Y-%m-%dT%H:%M:%S")

    logging.info(f"Data de início: {start_date}")
    logging.info(f"Data de fim: {end_date}")

    if not auth_test():
        logging.error("Autenticação falhou. O processo será interrompido.")
    else:
        conversations = fetch_all_conversations(start_date, end_date)
        data_processed = enrich_contacts_with_client_data(conversations)

        save_to_csv(data_processed)

        logging.info("Processo concluído.")
