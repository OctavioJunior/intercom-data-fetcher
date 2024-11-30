import logging
import pickle
import os
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

ID_DRIVE_FOLDER = os.getenv("ID_DRIVE_FOLDER").strip()


def merge_csv(file_path, existing_csv_path):
    """Mescla dois arquivos CSV."""
    if not isinstance(file_path, str) or not isinstance(existing_csv_path, str):
        logging.error(
            f"Um dos caminhos fornecidos não é válido: file_path={file_path}, existing_csv_path={existing_csv_path}"
        )
        return

    logging.info(f"Lendo dados do arquivo local: {file_path}...")
    try:
        new_data = pd.read_csv(file_path)
        existing_data = pd.read_csv(existing_csv_path)
    except Exception as e:
        logging.error(f"Erro ao ler arquivos CSV: {e}")
        return

    logging.info("Mesclando dados...")
    merged_data = pd.concat([existing_data, new_data], ignore_index=True)
    merged_data.drop_duplicates(inplace=True)

    logging.info(f"Salvando o arquivo mesclado em: {existing_csv_path}")
    try:
        merged_data.to_csv(existing_csv_path, index=False)
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo CSV: {e}")


def upload_to_drive(file_path, file_name):
    logging.info("Iniciando o processo de upload para o Google Drive...")

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None

    base_path = os.path.dirname(__file__)
    credentials_path = os.path.join(base_path, "credentials.json")
    token_path = os.path.join(base_path, "token.pickle")

    if not os.path.exists(credentials_path):
        logging.error(f"Arquivo de credenciais {credentials_path} não encontrado!")
        return

    if not os.path.exists(token_path):
        logging.error(f"Arquivo de token {token_path} não encontrado!")
        return

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    folder_id = ID_DRIVE_FOLDER

    # Caminho temporário para armazenar o arquivo existente
    temp_existing_csv_path = "existing_file.csv"

    # Verificar e remover o arquivo existente
    if os.path.exists(temp_existing_csv_path):
        try:
            os.remove(temp_existing_csv_path)
            logging.info(f"Arquivo temporário {temp_existing_csv_path} removido.")
        except Exception as e:
            logging.warning(f"Erro ao remover {temp_existing_csv_path}: {e}")

    # Buscar o arquivo existente no Google Drive
    logging.info(f"Procurando por arquivo existente: {file_name}...")
    query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
    results = (
        service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    items = results.get("files", [])

    try:
        if items:
            # Caso o arquivo exista
            file_id = items[0]["id"]
            logging.info(f"Arquivo encontrado. ID: {file_id}. Baixando...")

            request = service.files().get_media(fileId=file_id)
            existing_csv = BytesIO()
            downloader = MediaIoBaseDownload(existing_csv, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            existing_csv.seek(0)  # Move o ponteiro para o início do arquivo

            with open(temp_existing_csv_path, "wb") as f:
                f.write(existing_csv.read())

            logging.info(f"Arquivo {temp_existing_csv_path} baixado com sucesso.")

            # Mesclar os arquivos
            if os.path.exists(file_path):
                logging.info("Arquivo local encontrado, iniciando processamento...")
                merge_csv(file_path, temp_existing_csv_path)
            else:
                logging.error(f"Arquivo {file_path} não encontrado ou indisponível.")

            # Atualizar o arquivo no Google Drive
            logging.info(f"Atualizando o arquivo {file_name} no Google Drive...")
            media = MediaFileUpload(
                temp_existing_csv_path, mimetype="application/vnd.ms-excel"
            )
            updated_file = (
                service.files().update(fileId=file_id, media_body=media).execute()
            )
            logging.info(f"Arquivo atualizado com sucesso. ID: {updated_file['id']}")
        else:
            # Caso o arquivo não exista
            logging.info(f"Arquivo não encontrado. Criando novo arquivo: {file_name}")
            file_metadata = {"name": file_name, "parents": [folder_id]}
            media = MediaFileUpload(file_path, mimetype="application/vnd.ms-excel")
            created_file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            logging.info(f"Arquivo criado com sucesso. ID: {created_file['id']}")
    finally:
        # Garantir que o arquivo temporário seja removido
        if os.path.exists(temp_existing_csv_path):
            try:
                os.remove(temp_existing_csv_path)
                logging.info(f"Arquivo temporário {temp_existing_csv_path} removido.")
            except Exception as e:
                logging.warning(f"Erro ao remover {temp_existing_csv_path}: {e}")
