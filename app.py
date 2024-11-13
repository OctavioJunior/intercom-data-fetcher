import requests
import pandas as pd
from datetime import datetime
import os
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
INTERCOM_TOKEN = os.getenv('INTERCOM_TOKEN')

if not INTERCOM_TOKEN:
    raise ValueError("O token INTERCOM_TOKEN não foi encontrado. Verifique seu arquivo .env.")

# Configurações da API
API_URL = 'https://api.intercom.io/conversations/search'
INTERCOM_VERSION = '2.11'
RESULTADOS_POR_PAGINA = 150

# Cabeçalhos para a requisição
headers = {
    'Authorization': f'Bearer {INTERCOM_TOKEN}',
    'Content-Type': 'application/json',
    'Intercom-Version': INTERCOM_VERSION
}

# Configuração do log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para testar a autenticação
def testar_autenticacao():
    test_url = 'https://api.intercom.io/me'  # Endpoint de verificação de conta
    try:
        logging.info("Iniciando o teste de autenticação...")
        response = requests.get(test_url, headers=headers)
        response.raise_for_status()  # Verifica se houve erro
        logging.info("Autenticação bem-sucedida!")
    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro de autenticação: {e}")
        try:
            error_data = response.json()
            logging.error(f"Mensagem da API: {error_data}")
        except ValueError:
            logging.error(f"Erro na resposta da API: {response.text}")
        return False
    return True

# Função para converter uma data no formato 'YYYY-MM-DD HH:MM:SS' para timestamp Unix
def date_to_timestamp(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return int(date_obj.timestamp())

# Função para ajustar as datas
def adjust_dates(start_date_str, end_date_str):
    # Ajusta a start_date para 00:00:00
    start_date = f"{start_date_str} 00:00:00"
    # Ajusta a end_date para 23:59:59
    end_date = f"{end_date_str} 23:59:59"
    
    logging.info(f"Data inicial ajustada para: {start_date}")
    logging.info(f"Data final ajustada para: {end_date}")
    
    return start_date, end_date

# Função para buscar dados paginados
def fetch_all_conversations(start_date, end_date):
    # Ajusta as datas
    start_date, end_date = adjust_dates(start_date, end_date)
    
    # Converte as datas para timestamps
    start_timestamp = date_to_timestamp(start_date)
    end_timestamp = date_to_timestamp(end_date)

    # Estrutura de dados para armazenar todas as conversas
    all_conversations = []

    # Configura o payload inicial da requisição
    payload = {
        "query": {
            "operator": "AND",
            "value": [
                {"field": "created_at", "operator": ">", "value": start_timestamp},
                {"field": "created_at", "operator": "<", "value": end_timestamp}
            ]
        },
        "pagination": {"per_page": RESULTADOS_POR_PAGINA}
    }

    # Paginação - Loop para pegar todas as páginas
    page = 1
    while True:
        logging.info(f"Iniciando requisição para a página {page}...")

        response = requests.post(API_URL, json=payload, headers=headers)
        try:
            response.raise_for_status()  # Verifica se houve erro
            data = response.json()
            logging.info(f"Requisição bem-sucedida para a página {page}.")
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro na requisição na página {page}: {e}")
            try:
                error_data = response.json()
                logging.error(f"Mensagem da API: {error_data}")
            except ValueError:
                logging.error(f"Erro na resposta da API: {response.text}")
            break  # Encerra o loop em caso de erro

        # Adiciona os resultados da página atual
        conversations = data.get('conversations', [])
        logging.info(f"Página {page}: {len(conversations)} conversas encontradas.")
        # all_conversations.extend(conversations)

        # Filtra as informações desejadas
        for conversation in conversations:
          conversation_info = {
              'Conversation id': conversation.get('id'),
              'Conversation status': conversation.get('state'),
              'tags': [tag.get('name') for tag in conversation.get('tags', {}).get('tags', [])],
              'Created at': conversation.get('created_at'),
              'Last updated at': conversation.get('updated_at'),
              'Reopened': conversation.get('statistics', {}).get('count_reopens', 0),
              '???Closed': conversation.get('statistics', {}).get('count_reopens', 0) + 1,
              'Conversation rating': conversation.get('conversation_rating'),
              'Email': conversation.get('source', {}).get('author', {}).get('email'),
              'Name': conversation.get('source', {}).get('author', {}).get('name'),
              'Type': conversation.get('source', {}).get('author', {}).get('type'),
              'Participated (ID)': conversation.get('contacts', {}).get('contacts', [{}])[0].get('external_id', 'null'),
              '???Participated (name)': conversation.get('source', {}).get('author', {}).get('name'),
              '???Participated (name)': conversation.get('source', {}).get('author', {}).get('email'),
              '???User ID': conversation.get('contacts', {}).get('contacts', [{}])[0].get('external_id', 'null'),
              'Assigned to (ID)': conversation.get('team_assignee_id'),
              'Closed by (ID)': conversation.get('statistics', {}).get('last_closed_by_id'),
          }
          all_conversations.append(conversation_info)

        # Verifica se há uma próxima página (se existe o cursor starting_after)
        starting_after = data.get('pages', {}).get('next', {}).get('starting_after')
        if not starting_after:
            logging.info("Nenhuma próxima página encontrada. Encerrando o processo de busca.")
            break  # Sai do loop se não houver mais páginas

        # Atualiza o payload com o cursor da próxima página
        payload['pagination']['starting_after'] = starting_after
        page += 1

    logging.info(f"Total de conversas encontradas: {len(all_conversations)}.")
    return all_conversations

# Função para salvar os dados em CSV
def save_to_csv(conversations, file_name='conversas_intercom.csv'):
    if not conversations:
        logging.warning("Nenhuma conversa encontrada para salvar.")
        return

    # Converte para DataFrame
    df = pd.json_normalize(conversations)
    
    # Salva em CSV
    file_path = os.path.join(os.getcwd(), file_name)
    df.to_csv(file_path, index=False)
    logging.info(f"Arquivo CSV salvo em: {file_path}")

# Executa o fluxo completo
if __name__ == '__main__':
    logging.info("Iniciando o processo de busca de conversas no Intercom.")

    # Testa a autenticação
    if not testar_autenticacao():
        logging.error("Autenticação falhou. O processo será interrompido.")
    else:
        logging.info("Autenticação bem-sucedida. Continuando com a busca de conversas.")

        start_date = "2024-01-01"  # Exemplo: data de início
        end_date = "2024-01-01"    # Exemplo: data de fim

        # Busca todas as conversas e salva em CSV
        conversations = fetch_all_conversations(start_date, end_date)
        save_to_csv(conversations)

        logging.info("Processo concluído.")
