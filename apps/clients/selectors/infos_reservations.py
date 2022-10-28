import contextlib

from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any, Callable, List, Literal, Optional, Tuple, TypedDict, Union,
)

from django.db import models

from apps.clients.models import (
    OtherInfoReservation, Passenger, SeletectedJourney,
)
from utils.base_model import PersonneGenderBase

SESSION_INVALID = "Session invalide"

RETURN_TYPE = Union[Tuple[Literal[True], Any], Tuple[Literal[False], str]]


class ParamsTitleFullName(TypedDict):
    gender: str
    title: str


type_name = {
    PersonneGenderBase.MAN: "Mr",
    PersonneGenderBase.WOMAN: "Mme",
    PersonneGenderBase.INDERTEMINAT: "Mr/Mme"
}


def title_fullname(gender: str, fullname: str):
    title = type_name.get(gender, "Mr")
    return f"{title} {fullname}"


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
    title_fullname: Callable[[ParamsTitleFullName], str] = field(init=False)
    send_ticket_callback: Optional[Callable[[Any], bool]]
    session: str = field(init=False)
    error: Union[str, None] = field(init=False)
    reservation: SeletectedJourney = field(init=False)
    queryset = SeletectedJourney.objects.all()

    # relation models
    related = ("journey", "session", "journey_class", "other_info")
    prefetch = ("passengers",)

    def get_queryset(self, session: Optional[str] = None):
        return self.queryset.filter(
            session__key=session or self.session
        ).select_related(*self.related).prefetch_related(*self.prefetch)

    def reservation_progression(self):
        return self.reservation

    def get_passengers(self) -> list:
        if (
            hasattr(self.reservation, "passengers") and
            hasattr(self.reservation.passengers, "all")  # type: ignore
        ):
            return self.reservation.passengers.all()  # type: ignore
        return []

    def get_other_info(self) -> Optional[OtherInfoReservation]:
        with contextlib.suppress(OtherInfoReservation.DoesNotExist):
            if hasattr(self.reservation, "other_info"):
                return self.reservation.other_info  # type: ignore

    def booker(self) -> str:
        """ fullname of booker """
        if other_info := self.get_other_info():
            return title_fullname(
                gender=other_info.gender,
                fullname=other_info.fullname
            )
        return "-"

    def reservation_completed(self):
        """
        booker: str,
        expire_datetime: Date,
        pnr: str,
        total_price: 20000 Fc,
        text_reservation:str
        passengers: str[]
        """
        tmp_passengers = self.get_passengers()
        passengers: List[str] = [
            title_fullname(
                gender=passenger.gender,
                fullname=passenger.fullname
            ) for passenger in tmp_passengers
        ]

        self.send_ticket()
        return OrderedDict(
            booker=self.booker(),
            expire_datetime=self.reservation.session.date_expiration,
            pnr=self.reservation.pnr,
            passengers=passengers,
            total_price="",
            text_reservation="",
        )

    def send_ticket(self, *args, **kwargs):
        """ sending ticket to booker"""
        if self.send_ticket_callback:
            self.send_ticket_callback(self.reservation)

    def is_valide(self, session: Optional[str] = None) -> bool:
        with contextlib.suppress(SeletectedJourney.DoesNotExist):
            self.reservation = self.get_queryset(session=session).get()
            return True
        self.error = SESSION_INVALID
        return False

    def reset_error(self) -> None:
        self.error = None


def send_ticket(*args, **kwargs) -> bool:
    print("send_ticket ====>", args, kwargs)
    return True


# Info Reservation Info
reservation = InfoReservation(send_ticket_callback=send_ticket)


def reservation_progression(
    session: str
) -> Union[Tuple[Literal[True], Any], Tuple[Literal[False], str]]:

    if reservation.is_valide(session=session):
        return True, reservation.reservation_progression()
    return False, reservation.error or SESSION_INVALID


def reservation_completed(session: str) -> RETURN_TYPE:
    if reservation.is_valide(session=session):
        return True, reservation.reservation_completed()
    return False, reservation.error or SESSION_INVALID
