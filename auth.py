import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

INTERCOM_TOKEN = os.getenv("INTERCOM_TOKEN")
API_URL_AUTH = os.getenv("API_URL_AUTH")

if not INTERCOM_TOKEN:
    raise ValueError(
        "O token INTERCOM_TOKEN não foi encontrado. Verifique seu arquivo .env."
    )

INTERCOM_TOKEN = INTERCOM_TOKEN.strip()

headers = {
    "Authorization": f"Bearer {INTERCOM_TOKEN}",
    "Content-Type": "application/json",
    "Intercom-Version": "2.11",
}


def auth_test():
    test_url = API_URL_AUTH.strip()
    try:
        logging.info("Iniciando o teste de autenticação...")
        logging.info(f"Token: {INTERCOM_TOKEN[:10]}...")
        response = requests.get(test_url, headers=headers)
        response.raise_for_status()
        logging.info("Autenticação bem-sucedida!")
        return True
    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro de autenticação: {e}")
        return False
