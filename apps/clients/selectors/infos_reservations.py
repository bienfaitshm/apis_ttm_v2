from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Literal, Tuple, Union

from django.db import models

from apps.clients.models import SeletectedJourney

SESSION_INVALID = "Session invalide"


class StepReservation:
    SELECT = 0
    PASSENGER = 1
    OTHER_INFO = 2
    CONFIRMATION = 3


@dataclass
class StepInfoQuery:
    def getStep(self):
        #
        pass


@dataclass
class InfoReservation:
    session: str
    journey_query = SeletectedJourney.objects.all()
    related = ("journey", "session", "journey_class")

    def progression_queryset(self):
        return self.journey_query.filter(
            session__key=self.session
        ).select_related(*self.related)

    def reservation_progression(self):
        data = self.progression_queryset().prefetch_related("passengers").first()
        print(data)
        # return {
        #     "passengers": OrderedDict(adult=2, child=1, inf=2)
        # }

        return data

    def is_valide(self) -> bool:
        return self.progression_queryset().exists()

    @property
    def error(self):
        return SESSION_INVALID


def reservation_progression(
    session: str
) -> Union[Tuple[Literal[True], Any], Tuple[Literal[False], str]]:
    reservation = InfoReservation(session=session)
    if reservation.is_valide():
        return True, reservation.reservation_progression()
    return False, reservation.error
