import string

from datetime import date, datetime, time
from typing import Any, List, Optional, TypedDict

from django.utils.crypto import get_random_string

from apps.clients.models import Passenger
from apps.dash.models import Journey
from utils.times import cobine_date_n_time, get_now


class TNTypeUser(TypedDict):
    adult: int
    child: int
    baby: int


def pnr_creator(*args, **kwargs):
    """create png function"""
    return get_random_string(6, string.ascii_uppercase)


def key_session_creator(*args, **kwargs):
    return get_random_string(20, string.ascii_letters)


# time conbiner
def combiner_datetime(date: Optional[date], time: Optional[time]) -> datetime:
    return cobine_date_n_time(date=date, time=time) if (date and time) else get_now()


def clone_value(obj: Any, addons: Optional[dict] = None) -> dict:
    """Returns a clone of this instance."""
    if addons is None:
        addons = {}
    data = {f.attname: getattr(obj, f.attname)
            for f in obj.__class__._meta.fields}
    return {**data, **addons}


def nps_by_type(passengers: List[Passenger]) -> TNTypeUser:
    adult = 0
    child = 0
    baby = 0
    for passenger in passengers:
        if passenger.typeUser == Passenger.BABY:
            baby += 1
        if passenger.typeUser == Passenger.CHILD:
            child += 1
        if passenger.typeUser == Passenger.ADULT:
            adult += 1
    return {"adult": adult, "child": child, "baby": baby}
