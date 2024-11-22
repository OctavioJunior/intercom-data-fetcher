import logging
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_to_drive(file_path, file_name):
    logging.info("Iniciando o processo de upload para o Google Drive...")

    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    creds = None

    # Caminhos relativos para os arquivos de credenciais e token
    base_path = os.path.dirname(__file__)
    credentials_path = os.path.join(base_path, "credentials.json")
    token_path = os.path.join(base_path, "token.pickle")

    # Verificar se os arquivos necessários existem
    if not os.path.exists(credentials_path):
        logging.error(f"Arquivo de credenciais {credentials_path} não encontrado!")
        return  # Interrompe a execução se o arquivo não for encontrado

    if not os.path.exists(token_path):
        logging.error(f"Arquivo de token {token_path} não encontrado!")
        return  # Interrompe a execução se o arquivo não for encontrado

    # Carregar o token se ele existir
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
