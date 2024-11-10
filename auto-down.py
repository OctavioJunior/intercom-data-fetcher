import os
import pickle
import requests
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuração do arquivo CSV
csv_url = "https://www.football-data.co.uk/new/BRA.xlsx"
download_folder = "C:\\Users\\octav\\Downloads"
file_name = "BRA.xlsx"
file_path = os.path.join(download_folder, file_name)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cabeçalhos para a requisição HTTP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Função para baixar o arquivo CSV
def download_csv():
    logging.info("Iniciando o download do arquivo CSV...")
    try:
        response = requests.get(csv_url, headers=headers)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            logging.info(f"Arquivo CSV baixado com sucesso em: {file_path}")
        else:
            logging.error(f"Erro ao baixar o arquivo. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de requisição ao baixar o arquivo: {e}")

# Função para autenticação e upload para o Google Drive
def upload_to_drive():
    logging.info("Iniciando o processo de upload para o Google Drive...")

    # Scopes necessários para o acesso ao Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = None
    # O arquivo token.pickle armazena o token de acesso do usuário e é criado automaticamente na primeira execução
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Se não houver credenciais válidas, permita o usuário se autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_new.json',  # Novo arquivo de credenciais
                SCOPES
                )
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para a próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Construa o serviço do Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Fazendo upload do arquivo
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/vnd.ms-excel')

    try:
        logging.info(f"Iniciando o upload do arquivo {file_name} para o Google Drive...")
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"Arquivo enviado com sucesso para o Google Drive. ID: {file['id']}")
    except Exception as e:
        logging.error(f"Erro ao fazer upload para o Google Drive: {e}")

if __name__ == "__main__":
    # Baixar o arquivo CSV
    download_csv()

    # Fazer upload no Google Drive
    upload_to_drive()
