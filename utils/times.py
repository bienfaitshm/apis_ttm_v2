from datetime import datetime, timedelta


def get_date_expiration(date_dep: datetime) -> datetime:
    now = datetime.now()
    weeks_tow_diff = now + timedelta(days=14)
    hours_3_diff = now + timedelta(days=3)
    if date_dep > weeks_tow_diff:
        return now + timedelta(days=7)
    if date_dep > hours_3_diff:
        return now + timedelta(hours=12)
    return now + timedelta(hours=3)
