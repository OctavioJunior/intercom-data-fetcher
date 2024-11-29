import logging
import sys
from dotenv import load_dotenv
from auth import auth_test
from api_intercom import fetch_all_conversations
from save_file import save_to_csv
from fetch_client import enrich_contacts_with_client_data
from upload_to_drive import upload_to_drive
import os
from logging_config import setup_logging
from date_utils import get_date_range


def main():

    logging.info("Iniciando o processo de busca de conversas no Intercom.")

    start_date, end_date = get_date_range()
    # start_date = "2024-01-01T00:00:00"
    # end_date = "2024-01-01T23:59:59"
    logging.info(f"Data de início: {start_date}")
    logging.info(f"Data de fim: {end_date}")

    if not auth_test():
        logging.error("Autenticação falhou. O processo será interrompido.")
        return

    try:
        conversations = fetch_all_conversations(start_date, end_date)

        clients_data = enrich_contacts_with_client_data(conversations)

        date_prefix = start_date[:10]

        file_path, file_name = save_to_csv(
            clients_data, file_name_prefix=f"{date_prefix}"
        )

        if file_path and file_name:
            logging.info(f"Arquivo pronto para o upload: {file_name}")
            upload_to_drive(file_path, file_name)
        else:
            logging.error("Erro ao salvar o arquivo. Upload não realizado.")

    except Exception as e:
        logging.error(f"Ocorreu um erro durante o processamento: {e}")

    logging.info("Processo concluído.")


if __name__ == "__main__":
    base_path = (
        os.path.dirname(os.path.abspath(__file__))
        if not getattr(sys, "frozen", False)
        else sys._MEIPASS
    )
    load_dotenv(os.path.join(base_path, ".env"))
    setup_logging()
    main()
