
from __future__ import annotations
from datetime import datetime, timedelta

def monday_of_week(date_in: datetime | str, days_back: int = 0) -> tuple[str, str]:
    if isinstance(date_in, datetime):
        d = date_in
    else:
        d = datetime.strptime(date_in, '%Y-%m-%d')
    d = d - timedelta(days=days_back)
    monday = d - timedelta(days=d.weekday())
    return monday.strftime('%Y-%m-%d'), str(monday.isocalendar()[1])


def weeks_between(start_date: str, end_date: str) -> int:
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
    return int((d2 - d1).days // 7)


def to_date_and_cw(iso_str: str) -> tuple[str, str | None]:
    try:
        s = iso_str.rstrip('Z') if isinstance(iso_str, str) else ''
        dt = datetime.fromisoformat(s)
        return dt.strftime('%Y-%m-%d'), dt.strftime('%y%U')
    except Exception:
        return 'No Date', None
    
def date_of_now(date_in: datetime | None = None) -> tuple[str, str]:
    if date_in is None:
        date_in = datetime.now()
    return date_in.strftime('%Y-%m-%d'), str(date_in.isocalendar()[1])

def date_of_now_detail(date_in: datetime | None = None) -> tuple[str, str]:
    if date_in is None:
        date_in = datetime.now()
    return date_in.strftime('%Y-%m-%d_%H%M%S')
