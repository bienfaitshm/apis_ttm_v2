import inspect

from datetime import datetime, timedelta
from typing import Any, Callable

FuncGetNowType = Callable[[], datetime]


def get_now() -> datetime:
    return datetime.now()

# def get_diff_datetime(date1:datetime, date2:datetime)->datetime:
#     return date1.now() - date2.now()


def cobine_date_n_time(date: Any, time: Any) -> datetime:
    """combine date and time to datetime"""
    return datetime.combine(date=date, time=time)


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
    if not inspect.isfunction(from_date):
        raise AttributeError("from_date is not a function or callable.")
    now = from_date()
    return date_time > now if isinstance(date_time, datetime) else True
