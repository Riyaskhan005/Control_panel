from datetime import datetime, timezone

def get_current_utc():
    current_utc_datetime = datetime.now(timezone.utc)
    formatted_utc_string = current_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_utc_string
