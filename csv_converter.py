from date_utils import convert_timestamp, convert_seconds_to_minutes


def csv_converter(conversations):
    expanded_conversations = []

    for conversation in conversations:

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
            "source_delivered_as": safe_get(
                conversation.get("source", {}), "delivered_as"
            ),
            "source_subject": safe_get(conversation.get("source", {}), "subject"),
            "author_type": safe_get(
                conversation.get("source", {}).get("author", {}), "type"
            ),
            "author_id": safe_get(
                conversation.get("source", {}).get("author", {}), "id"
            ),
            "author_name": safe_get(
                conversation.get("source", {}).get("author", {}), "name"
            ),
            "author_email": safe_get(
                conversation.get("source", {}).get("author", {}), "email"
            ),
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
            "statistics_time_to_assignment": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "time_to_assignment", 0)
            ),
            "statistics_time_to_admin_reply": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "time_to_admin_reply", 0)
            ),
            "statistics_time_to_first_close": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "time_to_first_close", 0)
            ),
            "statistics_time_to_last_close": convert_seconds_to_minutes(
                safe_get(conversation.get("statistics", {}), "time_to_last_close", 0)
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
            "statistics_first_close_at": convert_timestamp(
                safe_get(conversation.get("statistics", {}), "first_close_at")
            ),
            "statistics_last_assignment_at": convert_timestamp(
                safe_get(conversation.get("statistics", {}), "last_assignment_at")
            ),
            "statistics_last_assignment_admin_reply_at": convert_timestamp(
                safe_get(
                    conversation.get("statistics", {}),
                    "last_assignment_admin_reply_at",
                )
            ),
            "statistics_last_contact_reply_at": convert_timestamp(
                safe_get(
                    conversation.get("statistics", {}),
                    "last_contact_reply_at",
                )
            ),
            "statistics_last_admin_reply_at": convert_timestamp(
                safe_get(
                    conversation.get("statistics", {}),
                    "last_admin_reply_at",
                )
            ),
            "statistics_last_close_at": convert_timestamp(
                safe_get(
                    conversation.get("statistics", {}),
                    "last_close_at",
                )
            ),
            "statistics_last_closed_by_id": convert_seconds_to_minutes(
                safe_get(
                    conversation.get("statistics", {}),
                    "last_closed_by_id",
                )
            ),
            "statistics_count_reopens": safe_get(
                conversation.get("statistics", {}), "count_reopens"
            ),
            "statistics_count_assignments": safe_get(
                conversation.get("statistics", {}), "count_assignments"
            ),
            "statistics_count_conversation_parts": safe_get(
                conversation.get("statistics", {}), "count_conversation_parts"
            ),
            "conversation_rating": safe_get(conversation, "conversation_rating"),
            "contact_client_id": safe_get(conversation.get("contact_info", {}), "id"),
            "contact_name": safe_get(conversation.get("contact_info", {}), "name"),
            "contact_phone": safe_get(conversation.get("contact_info", {}), "phone"),
            "contact_email": safe_get(conversation.get("contact_info", {}), "email"),
            "contact_role": safe_get(conversation.get("contact_info", {}), "role"),
            "contact_has_hard_bounced": safe_get(
                conversation.get("contact_info", {}), "has_hard_bounced"
            ),
            "contact_marked_email_as_spam": safe_get(
                conversation.get("contact_info", {}), "marked_email_as_spam"
            ),
            "contact_unsubscribed_from_emails": safe_get(
                conversation.get("contact_info", {}), "unsubscribed_from_emails"
            ),
            "contact_created_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "created_at")
            ),
            "contact_updated_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "updated_at")
            ),
            "contact_signed_up_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "signed_up_at")
            ),
            "contact_last_seen_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "last_seen_at")
            ),
            "contact_last_replied_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "last_replied_at")
            ),
            "contact_last_contacted_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "last_contacted_at")
            ),
            "contact_last_email_opened_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "last_email_opened_at")
            ),
            "contact_last_email_clicked_at": convert_timestamp(
                safe_get(conversation.get("contact_info", {}), "last_email_clicked_at")
            ),
            "location_city": safe_get(
                conversation.get("contact_info", {}).get("location", {}), "city"
            ),
            "location_region": safe_get(
                conversation.get("contact_info", {}).get("location", {}), "region"
            ),
            "location_country": safe_get(
                conversation.get("contact_info", {}).get("location", {}), "country"
            ),
            "android_app_name": safe_get(
                conversation.get("contact_info", {}), "android_app_name"
            ),
            "android_device": safe_get(
                conversation.get("contact_info", {}), "android_device"
            ),
            "ios_app_name": safe_get(
                conversation.get("contact_info", {}), "ios_app_name"
            ),
            "ios_device": safe_get(conversation.get("contact_info", {}), "ios_device"),
        }

        expanded_conversations.append(conv_data)

    return expanded_conversations
