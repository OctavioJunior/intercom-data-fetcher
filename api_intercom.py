import os
import requests
import logging
from auth import headers
from dotenv import load_dotenv
from date_utils import normalize_date_format, date_to_timestamp, normalize_date_format

load_dotenv()

API_URL_CONVERSATION = os.getenv("API_URL_CONVERSATION")
RESULTS_PER_PAGE = int(os.getenv("RESULTS_PER_PAGE", 150))

API_URL_CONVERSATION = API_URL_CONVERSATION.strip()


def fetch_all_conversations(start_date, end_date):

    start_date = normalize_date_format(start_date)
    end_date = normalize_date_format(end_date)

    logging.info(f"Data inicial normalizada: {start_date}")
    logging.info(f"Data final normalizada: {end_date}")

    start_timestamp = date_to_timestamp(start_date)
    end_timestamp = date_to_timestamp(end_date)

    all_conversations = []
    payload = {
        "query": {
            "operator": "AND",
            "value": [
                {"field": "created_at", "operator": ">", "value": start_timestamp},
                {"field": "created_at", "operator": "<", "value": end_timestamp},
            ],
        },
        "pagination": {"per_page": RESULTS_PER_PAGE},
    }

    page = 1
    while True:
        logging.info(f"Iniciando requisição para a página {page}...")
        response = requests.post(
            API_URL_CONVERSATION, json=payload, headers=headers, timeout=30
        )
        logging.info(f"Status da resposta da página {page}: {response.status_code}")
        try:
            response.raise_for_status()
            data = response.json()
            conversations = data.get("conversations", [])
            logging.info(f"Página {page}: {len(conversations)} conversas encontradas.")
            all_conversations.extend(conversations)
        except requests.exceptions.HTTPError as e:
            logging.error(f"Erro na requisição na página {page}: {e}")
            break

        starting_after = data.get("pages", {}).get("next", {}).get("starting_after")
        if not starting_after:
            logging.info(f"Sem mais páginas. Finalizando a busca.")
            break

        payload["pagination"]["starting_after"] = starting_after
        page += 1

    return all_conversations
