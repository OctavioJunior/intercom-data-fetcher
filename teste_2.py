import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
INTERCOM_TOKEN = os.getenv('INTERCOM_TOKEN')

if not INTERCOM_TOKEN:
    raise ValueError("O token INTERCOM_TOKEN não foi encontrado. Verifique seu arquivo .env.")

# Configurações da API
INTERCOM_VERSION = '2.11'
EXPORT_ENDPOINT = 'https://api.intercom.io/export/content/data'
CHECK_JOB_ENDPOINT = lambda job_id: f'https://api.intercom.io/export/content/data/{job_id}'
DOWNLOAD_JOB_ENDPOINT = lambda job_id: f'https://api.intercom.io/download/content/data/{job_id}'

# Função para converter data para timestamp Unix (agora aceita hora também)
def date_to_timestamp(date_str):
    # Ajuste para lidar com data e hora no formato "YYYY-MM-DD HH:MM:SS"
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(date_obj.timetuple()))

# Função para criar o job de exportação
def create_export_job(start_date, end_date):
    headers = {
        'Authorization': f'Bearer {INTERCOM_TOKEN}',
        'Content-Type': 'application/json',
        'Intercom-Version': INTERCOM_VERSION
    }
    data = {
        'created_at_after': start_date,
        'created_at_before': end_date
    }
    response = requests.post(EXPORT_ENDPOINT, json=data, headers=headers)
    response.raise_for_status()
    return response.json().get('job_identifier')

# Função para verificar o status do job
def check_job_status(job_id):
    headers = {
        'Authorization': f'Bearer {INTERCOM_TOKEN}',
        'Intercom-Version': INTERCOM_VERSION
    }
    response = requests.get(CHECK_JOB_ENDPOINT(job_id), headers=headers)
    response.raise_for_status()
    return response.json()

# Função para fazer o download do CSV
def download_csv(job_id, file_path):
    headers = {
        'Authorization': f'Bearer {INTERCOM_TOKEN}',
        'Intercom-Version': INTERCOM_VERSION,
        'Accept': 'application/octet-stream'
    }
    response = requests.get(DOWNLOAD_JOB_ENDPOINT(job_id), headers=headers, stream=True)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return file_path

# Função principal para executar o fluxo de exportação completo
def export_data_flow(start_date_str, end_date_str):
    try:
        # Passo 1: Converter as datas para timestamp
        start_date = date_to_timestamp(start_date_str)
        end_date = date_to_timestamp(end_date_str)
        print(f'Datas convertidas: {start_date} - {end_date}')

        # Passo 2: Criar o job de exportação
        print('Criando o job de exportação...')
        job_id = create_export_job(start_date, end_date)
        print(f'Job criado com ID: {job_id}')

        # Passo 3: Verificar o status até estar completo
        while True:
            print('Verificando status do job...')
            job_data = check_job_status(job_id)
            job_status = job_data.get('status')
            if job_status == 'completed':
                print('Job concluído com sucesso.')
                break
            elif job_status == 'failed':
                raise Exception('O job falhou.')
            else:
                print(f'Status atual do job: {job_status}. Tentando novamente em 5 segundos...')
                time.sleep(5)

        # Passo 4: Fazer o download do CSV
        file_path = os.path.join(os.getcwd(), 'exported_data.csv.gz')
        print('Fazendo o download do CSV...')
        download_csv(job_id, file_path)
        print(f'Download concluído. Arquivo salvo em: {file_path}')
    except Exception as e:
        print(f'Erro no processo de exportação: {e}')

# Executa o fluxo com as datas especificadas (com hora incluída)
export_data_flow("2024-01-01 00:00:00", "2024-01-31 23:59:59")
