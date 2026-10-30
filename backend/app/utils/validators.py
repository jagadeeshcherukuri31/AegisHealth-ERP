from datetime import date, datetime


def require_fields(data, *fields):
    data = data or {}
    missing = [f for f in fields if data.get(f) in (None, "")]
    if missing:
        raise ValueError("Missing required field(s): " + ", ".join(missing))
    return data


def parse_date(v):
    try:
        return date.fromisoformat(v)
    except (TypeError, ValueError):
        raise ValueError("Invalid date, expected YYYY-MM-DD")


def parse_dt(v):
    try:
        return datetime.fromisoformat(v)
    except (TypeError, ValueError):
        raise ValueError("Invalid datetime, expected ISO 8601")
