import logging
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


def upload_to_drive(file_path, file_name):
    logging.info("Iniciando o processo de upload para o Google Drive...")

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, mimetype="application/vnd.ms-excel")

    try:
        logging.info(
            f"Iniciando o upload do arquivo {file_name} para o Google Drive..."
        )
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        logging.info(
            f"Arquivo enviado com sucesso para o Google Drive. ID: {file['id']}"
        )
    except Exception as e:
        logging.error(f"Erro ao fazer upload para o Google Drive: {e}")
