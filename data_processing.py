import logging


def process_conversations(conversations):
    logging.info(f"Tratando dados do JSON")

    processed_data = []
    for conversation in conversations:
        conversation_info = {
            "Conversation id": conversation.get("id"),
            "Conversation status": conversation.get("state"),
            "tags": [
                tag.get("name") for tag in conversation.get("tags", {}).get("tags", [])
            ],
            "Created at": conversation.get("created_at"),
            "Last updated at": conversation.get("updated_at"),
            "Reopened": conversation.get("statistics", {}).get("count_reopens", 0),
            "Closed by (ID)": conversation.get("statistics", {}).get(
                "last_closed_by_id"
            ),
            "Email": conversation.get("source", {}).get("author", {}).get("email"),
            "Name": conversation.get("source", {}).get("author", {}).get("name"),
        }
        processed_data.append(conversation_info)
    return processed_data
