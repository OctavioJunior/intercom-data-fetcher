import os
import logging
import requests
from auth import headers
from dotenv import load_dotenv

load_dotenv()

API_URL_CONTACTS = os.getenv("API_URL_CONTACTS").strip()


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
    logging.info("Iniciando busca de contatos.")
    for conversation in conversations:
        contacts = conversation.get("contacts", {}).get("contacts", [])

        # Verifica se há pelo menos um contato
        if contacts:
            contact_id = contacts[0].get("id")
            if contact_id:
                client_details = fetch_client_details(contact_id)
                if client_details:
                    conversation["contact_info"] = client_details
                else:
                    conversation["contact_info"] = {
                        "error": "Detalhes do cliente não disponíveis"
                    }
            else:
                conversation["contact_info"] = {
                    "error": "ID do contato não encontrado."
                }
        else:
            conversation["contact_info"] = {
                "error": "Nenhum contato associado à conversa."
            }

    logging.info("Detalhes dos clientes obtidos com sucesso.")
    return conversations
