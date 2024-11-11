import os
import requests
import time
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Defina o token do Intercom (substitua pelo seu token)
INTERCOM_API_TOKEN = "YOUR_INTERCOM_API_TOKEN"
INTERCOM_VERSION = "2.11"
JOB_IDENTIFIER = "YOUR_JOB_IDENTIFIER"  # Você vai obter isso após a criação do job
DOWNLOAD_URL = "YOUR_DOWNLOAD_URL"  # Isso será obtido após o job ser concluído

# Google Drive Credentials (substitua pelo caminho do arquivo JSON de credenciais)
CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Função para autenticação no Google Drive
def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds, _ = load_credentials_from_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

# Função para verificar o status do job de exportação
def check_job_status(job_identifier):
    url = f"https://api.intercom.io/export/content/data/{job_identifier}"
    headers = {
        'Authorization': f'Bearer {INTERCOM_API_TOKEN}',
        'Intercom-Version': INTERCOM_VERSION
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao verificar o status do job: {response.status_code}")
        return None

# Função para baixar o arquivo
def download_file(download_url, save_path):
    headers = {
        'Authorization': f'Bearer {INTERCOM_API_TOKEN}',
        'Accept': 'application/octet-stream'
    }
    response = requests.get(download_url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Arquivo baixado com sucesso: {save_path}")
    else:
        print(f"Erro ao baixar o arquivo: {response.status_code}")

# Função para fazer o upload para o Google Drive
def upload_to_google_drive(file_path, file_name):
    service = authenticate_google_drive()
    folder_id = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # Substitua pela pasta desejada no Google Drive
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='application/gzip')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Arquivo enviado para o Google Drive com sucesso! ID do arquivo: {file['id']}")

# Função principal para controlar o fluxo da automação
def run_export_automation():
    # Passo 1: Verificar o status do job
    status = check_job_status(JOB_IDENTIFIER)
    
    if not status or status['status'] != 'completed':
        print("O job ainda não foi concluído.")
        return
    
    # Passo 2: Baixar o arquivo
    download_url = status['download_url']
    file_name = "export_data.csv.gz"  # Ou qualquer nome que desejar para o arquivo
    file_path = os.path.join(os.getcwd(), file_name)
    
    download_file(download_url, file_path)
    
    # Passo 3: Subir o arquivo para o Google Drive
    upload_to_google_drive(file_path, file_name)

# Agendamento mensal para rodar no dia 1
if __name__ == '__main__':
    # Aqui você pode usar algo como `schedule` ou `cron` para agendar a execução
    run_export_automation()
