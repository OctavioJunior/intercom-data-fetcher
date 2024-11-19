import os
import logging
import requests
from auth import headers
from dotenv import load_dotenv

load_dotenv()

API_URL_CONTACTS = os.getenv("API_URL_CONTACTS")


def fetch_client_details(client_id):

    api_url = f"{API_URL_CONTACTS}/{client_id}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        client_data = response.json()
        return client_data
    except requests.exceptions.HTTPError as e:
        logging.error(f"Erro ao buscar os detalhes do cliente {client_id}: {e}")
        return None


def enrich_contacts_with_client_data(conversations):

    logging.info(f"Iniciando busca de contatos.")
    for conversation in conversations:
        contacts = conversation.get("contacts", {}).get("contacts", [])

        client_data_list = []

        for contact in contacts:
            contact_id = contact.get("id")
            if contact_id:
                client_details = fetch_client_details(contact_id)
                if client_details:
                    client_data_list.append(client_details)
                else:
                    client_data_list.append(
                        {"error": "Detalhes do cliente não disponíveis"}
                    )
            else:
                logging.warning("ID do contato não encontrado.")

        conversation["data_client"] = client_data_list

    logging.info(f"Detalhes dos clientes obtidos com sucesso.")
    return conversations
