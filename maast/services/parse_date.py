from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[datetime.date]:
    try:
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except ValueError:
        return None
