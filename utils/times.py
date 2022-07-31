from datetime import datetime, timedelta
from typing import Callable

FuncGetNowType = Callable[[], datetime]


def get_now() -> datetime:
    return datetime.now()


def get_date_expiration(
    date_dep: datetime,
    from_date: FuncGetNowType = get_now
) -> datetime:
    """ get expiration of ..."""
    now = from_date()
    weeks_tow_diff = now + timedelta(days=14)
    hours_3_diff = now + timedelta(days=3)
    if date_dep > weeks_tow_diff:
        return now + timedelta(days=7)
    if date_dep > hours_3_diff:
        return now + timedelta(hours=12)
    return now + timedelta(hours=3)


def is_expired(
    date_time: datetime,
    from_date: FuncGetNowType = get_now
) -> bool:
    """  """
    now = from_date()
    if not isinstance(date_time, datetime):
        return True
    return date_time > now
