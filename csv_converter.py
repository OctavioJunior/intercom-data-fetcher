from date_utils import convert_timestamp, convert_seconds_to_minutes


def csv_converter(conversations):
    expanded_conversations = []

    for conversation in conversations:
        # Helper function to safely get values
        def safe_get(data, key, default=None):
            if isinstance(data, dict):
                return data.get(key, default)
            return default

        conv_data = {
            "conversation_id": safe_get(conversation, "id"),
            "created_at": convert_timestamp(safe_get(conversation, "created_at")),
            "updated_at": convert_timestamp(safe_get(conversation, "updated_at")),
            "waiting_since": safe_get(conversation, "waiting_since"),
            "snoozed_until": safe_get(conversation, "snoozed_until"),
            "source_type": safe_get(conversation.get("source", {}), "type"),
            "source_id": safe_get(conversation.get("source", {}), "id"),
            "contact_id": safe_get(
                (
                    conversation.get("contacts", {}).get("contacts", [])[0]
                    if conversation.get("contacts", {}).get("contacts")
                    else None
                ),
                "id",
            ),
            "contact_external_id": safe_get(
                (
                    conversation.get("contacts", {}).get("contacts", [])[0]
                    if conversation.get("contacts", {}).get("contacts")
                    else None
                ),
                "external_id",
            ),
            "first_contact_reply_created_at": convert_timestamp(
                safe_get(conversation.get("first_contact_reply", {}), "created_at")
            ),
            "first_contact_reply_type": safe_get(
                conversation.get("first_contact_reply", {}), "type"
            ),
            "admin_assignee_id": safe_get(conversation, "admin_assignee_id"),
            "team_assignee_id": safe_get(conversation, "team_assignee_id"),
            "open": safe_get(conversation, "open"),
            "state": safe_get(conversation, "state"),
            "read": safe_get(conversation, "read"),
            "priority": safe_get(conversation, "priority"),
            "statistics_time_to_admin_reply": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "time_to_admin_reply", 0)
            ),
            "statistics_median_time_to_reply": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "median_time_to_reply", 0)
            ),
            "statistics_first_contact_reply_at": convert_timestamp(
                safe_get(conversation.get("statistics", {}), "first_contact_reply_at")
            ),
            "statistics_first_assignment_at": convert_timestamp(
                safe_get(conversation.get("statistics", {}), "first_assignment_at")
            ),
            "statistics_first_admin_reply_at": convert_timestamp(
                safe_get(conversation.get("statistics", {}), "first_admin_reply_at")
            ),
            "conversation_rating": safe_get(conversation, "conversation_rating"),
            "contact_email": safe_get(conversation.get("contact_info", {}), "email"),
            "contact_phone": safe_get(conversation.get("contact_info", {}), "phone"),
            "contact_name": safe_get(conversation.get("contact_info", {}), "name"),
        }

        expanded_conversations.append(conv_data)

    return expanded_conversations
