"""
    48h=>3h
    >48h=>5h
    1semaine =>12h
    >2semaines => 24h
"""
from abc import ABC, abstractmethod
import string
from datetime import datetime
from typing import Any, List
from django.utils.crypto import get_random_string

from apps.dash.models import JourneyClass
from apps.dash.models.transport import Journey

from ..models import SeletectedJourney, JourneyClientFolder, JourneySession, Passenger, OtherInfoReservation


class ModelBaseProcess(ABC):
    """
    Base Of method implemention of process 
    Args:
        ABC (_type_): _description_

    Raises:
        Exception: _description_
    """
    @abstractmethod
    def create(self, *args, **kwargs):
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

    def __init__(self):
        self._selected_journey = SeletectedJourneyModelProcess()
        self._journey_session = JourneySessionModelProcess()
        self._folder = JourneyClientFolderModelProcess()

    def select_journey(self, *args, **kwargs):
        print(args, kwargs)
        session = self.get_session()
        folder = self.get_folder()
        selected = self._selected_journey.create(
            session=session,
            folder=folder,
            **kwargs
        )
        print("\t", dir(selected))
        return selected

    def addPassengers(self, jouney, passengers: List[Any]):
        Passenger.objects.bulk_create([
            Passenger(**i, journey=jouney) for i in passengers
        ])

        return Passenger.objects.filter(journey=jouney)

    def add_other_info(self, journey, other_info):
        return OtherInfoReservation.objects.create(journey=journey, **other_info)

    def get_folder(self, *args, **kwargs):
        return self._folder.create(
            number=get_random_string(6, string.digits),
            session=get_random_string(5, string.ascii_letters)
        )

    def get_session(self, *args, **kwargs):
        return self._journey_session.create(
            key=get_random_string(20, string.ascii_letters),
            date_expiration=datetime.now()
        )
