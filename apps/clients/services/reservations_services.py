import string
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string

from ..models import SeletectedJourney as Reservation, JourneySession, JourneyClientFolder


def _get_radom_string():
    return get_random_string(20, string.ascii_letters)


def _get_date_expiration(date_dep: any) -> any:
    now = datetime.now()
    weeks_tow_diff = now + timedelta(days=14)
    hours_3_diff = now + timedelta(days=3)
    if date_dep > weeks_tow_diff:
        return now + timedelta(days=7)
    if date_dep > hours_3_diff:
        return now + timedelta(hours=12)
    return now + timedelta(hours=3)


def create_pnr():
    """create png function"""
    return get_random_string(6, string.ascii_uppercase)


def create_reservation(journey, *args, **kwargs):
    date_dep = datetime.now()
    if hasattr(journey, "hoursDeparture") and hasattr(journey, "dateDeparture"):
        date_dep = datetime.combine(
            date=journey.dateDeparture, time=journey.hoursDeparture)

    session = create_session(date_dep)
    folder = create_folder()
    pnr = create_pnr()
    return Reservation.objects.create(
        session=session,
        folder=folder,
        journey=journey,
        pnr=pnr,
        * args, **kwargs)


def create_session(date_dep: any = None):
    date_exp = _get_date_expiration(date_dep)
    return JourneySession.objects.create(
        key=_get_radom_string(), date_expiration=date_exp
    )


def create_folder():
    return JourneyClientFolder.objects.create(
        number=get_random_string(6, string.digits),
        session=get_random_string(5, string.ascii_letters)
    )
