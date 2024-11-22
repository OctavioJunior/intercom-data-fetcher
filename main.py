import logging
from auth import auth_test
from api_intercom import fetch_all_conversations
from save_file import save_to_csv
from data_processing import enrich_contacts_with_client_data
from datetime import datetime, timedelta
import os
import sys
from dotenv import load_dotenv
from upload_to_drive import upload_to_drive
import platform


if platform.system() == "Windows":
    folder_path = os.path.join("C:", "intercom_data_fetcher", "files")
else:
    folder_path = os.path.join(os.getenv("HOME"), "intercom_data_fetcher", "files")

os.makedirs(folder_path, exist_ok=True)

log_path = os.path.join(folder_path, "log.txt")

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
file_handler = logging.FileHandler(log_path)

stdout_handler.setLevel(logging.INFO)
stderr_handler.setLevel(logging.ERROR)
file_handler.setLevel(logging.INFO)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[stdout_handler, stderr_handler, file_handler],
)

if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(base_path, ".env")

load_dotenv(dotenv_path)

if __name__ == "__main__":
    logging.info("Iniciando o processo de busca de conversas no Intercom.")

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

        date_prefix = start_date[:10]

        file_path, file_name = save_to_csv(
            data_processed, file_name_prefix=f"conversations_{date_prefix}"
        )

    if file_path and file_name:
        logging.info(f"Arquivo pronto para o upload: {file_name}")

        upload_to_drive(file_path, file_name)
    else:
        logging.error("Erro ao salvar o arquivo. Upload não realizado.")

        logging.info("Processo concluído.")
