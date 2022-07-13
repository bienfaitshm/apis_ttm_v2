"""
    48h=>3h
    >48h=>5h
    1semaine =>12h
    >2semaines => 24h
"""
from abc import ABC, abstractmethod
import string
from datetime import datetime, timedelta
from typing import Any, List
from django.utils.crypto import get_random_string

from apps.dash.models import JourneyClass
from apps.dash.models.transport import Journey

from ..models import SeletectedJourney, JourneyClientFolder, JourneySession, Passenger, OtherInfoReservation


def clone_and_value(obj, addons=None):
    """Returns a clone of this instance."""
    if addons is None:
        addons = {}
    data = {f.attname: getattr(obj, f.attname)
            for f in obj.__class__._meta.fields}
    return {**data, **addons}


class ModelBaseProcess(ABC):
    """
    Base Of method implemention of process 
    Args:
        ABC (_type_): _description_

    Raises:
        Exception: _description_
    """
    @abstractmethod
    def create(self, *args, **kwargs):  # sourcery skip: raise-specific-error
        raise Exception("method not implement")


class JourneySessionModelProcess(ModelBaseProcess):
    """
        JourneySession model Processing
    """
    model = JourneySession

    def create(self, *args, **kwargs):
        return self.model.objects.create(*args, **kwargs)


class SeletectedJourneyModelProcess(ModelBaseProcess):
    """
        SelectedJourney model Processing
    """
    model = SeletectedJourney

    def create(self, *args, **kwargs):
        return self.model.objects.create(*args, **kwargs)


class JourneyClientFolderModelProcess(ModelBaseProcess):
    """
        SelectedJourney model Processing
    """
    model = JourneyClientFolder

    def create(self, *args, **kwargs):
        return self.model.objects.create(*args, **kwargs)


class ReservationJourney:
    _session = None

    def get_key(self):
        return get_random_string(20, string.ascii_letters)

    def __init__(self):
        self._selected_journey = SeletectedJourneyModelProcess()
        self._journey_session = JourneySessionModelProcess()
        self._folder = JourneyClientFolderModelProcess()

    def select_journey(self, *args, **kwargs):
        session = self.get_session()
        folder = self.get_folder()
        return self._selected_journey.create(session=session, folder=folder, **kwargs)

    def addPassengers(self, jouney, passengers: List[Any]):
        Passenger.objects.bulk_create([
            Passenger(**i, journey=jouney) for i in passengers
        ])

        return Passenger.objects.filter(journey=jouney)

    def add_other_info(self, journey, other_info):
        existing_other_info = OtherInfoReservation.objects.filter(
            journey=journey)
        if not existing_other_info.exists():
            return OtherInfoReservation.objects.create(journey=journey, **other_info)
        return existing_other_info.first()

    def get_folder(self, *args, **kwargs):
        return self._folder.create(
            number=get_random_string(6, string.digits),
            session=get_random_string(5, string.ascii_letters)
        )

    def get_session(self, *args, **kwargs):
        # TODO temps de l'expiration de reservation et update les expirers

        return self._journey_session.create(
            **{"key": self.get_key(), "date_expiration": datetime.now(), **kwargs}
        )

    def splite_reservation(self, reservation, passengers, *args, **kwargs):
        res = SeletectedJourney.objects\
            .select_related("other_info", "session").get(pk=reservation.pk)

        n_passengers = get_number_type_user(passengers)

        new_session = self.get_session(
            clone_and_value(res.session, {"id": None}))

        new_reservation_data = clone_and_value(
            res, {"id": None, "session_id": new_session.pk, ** n_passengers})

        new_reservation = SeletectedJourney.objects.create(
            **new_reservation_data)

        if hasattr(res, "other_info"):
            new_data_other_info = clone_and_value(res.other_info)
            new_data_other_info.pop("journey_id")
            new_data_other_info.pop("id")
            self.add_other_info(new_reservation, new_data_other_info)

        ps = [i.pk for i in passengers]
        p = Passenger.objects.filter(pk__in=ps).update(journey=new_reservation)
        return new_reservation

    def void(self, reservation):
        return self._selected_journey.model.objects.filter(pk=reservation).update(status=SeletectedJourney.VOIDED)


def getOtherInfo(journey):
    passenger = Passenger.objects.filter(journey=journey)


def get_number_type_user(passengers: list[Passenger]):
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
