from datetime import datetime


def current_datetime_after_given_iso_string(value: str) -> bool:
    today = datetime.today().now()
    parsed = datetime.fromisoformat(value)
    return today > parsed


def current_datetime_before_given_iso_string(value: str) -> bool:
    today = datetime.today().now()
    parsed = datetime.fromisoformat(value)
    return today < parsed
