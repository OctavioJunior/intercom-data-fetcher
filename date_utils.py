from datetime import datetime, timedelta


def get_date_range():

    yesterday = datetime.now() - timedelta(1)
    start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_date.strftime("%Y-%m-%dT%H:%M:%S"), end_date.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )


def date_to_timestamp(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(date_obj.timestamp())


def normalize_date_format(date_str):

    if " " in date_str and date_str.count(":") > 3:
        date_str = date_str.rsplit(" ", 1)[0]

    date_str = date_str.replace("T", " ")

    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"Formato inválido detectado após normalização: {date_str}")

    return date_str


def convert_timestamp(timestamp):
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
    elif isinstance(timestamp, str):
        try:
            if timestamp.endswith("Z"):
                return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime(
                    "%d/%m/%Y"
                )
            else:
                return datetime.fromisoformat(timestamp).strftime("%d/%m/%Y")
        except ValueError:
            return timestamp
    return timestamp


def convert_seconds_to_minutes(seconds):
    if seconds is None:
        return None
    try:
        minutes = seconds // 60
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours:02d}:{remaining_minutes:02d}"
    except (ValueError, TypeError):
        return None
