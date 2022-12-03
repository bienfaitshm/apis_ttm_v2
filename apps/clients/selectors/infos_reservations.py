import contextlib

from collections import OrderedDict, namedtuple
from dataclasses import dataclass, field
from typing import (
    Any, Callable, List, Literal, Optional, Protocol, Tuple, Union,
)

from django.db import models

from apps.clients import models as c_models
from apps.clients.anotate import APassenger
from apps.clients.message import InfoJourneyMessage
from apps.clients.models import OtherInfoReservation, Passenger, Reservation
from apps.clients.selectors.selectors import (
    PriceSelector, PriceSelectorProtocol,
)
from apps.dash.models import Journey, JourneyTarif
from apps.dash.services.systems import IPriceSystem, PriceSystem
from systen.send_ticket import SendTicket
from utils import str_system

SESSION_INVALID = "Session invalide"

RETURN_TYPE = Union[Tuple[Literal[True], Any], Tuple[Literal[False], str]]


class TitleFullname(Protocol):
    def __call__(self, gender: str, fullname: str) -> str: ...


class TicketSender(Protocol):
    def send_ticket(self, *args, **kwargs) -> None: ...


# Progression object
Progression = namedtuple("Progression", [
    "adult", "child", "inf", "step", "passengers"
])


class StepReservation:
    SELECT = 0
    PASSENGER = 1
    OTHER_INFO = 2
    CONFIRMATION = 3


@dataclass
class PassengersQueries:
    tarif: PriceSelectorProtocol
    model = Passenger
    related = ("journey__journey",)

    def queryset(self):
        return self.model.objects.all()

    def anotate(self) -> dict:
        return {
            APassenger.TAXE: self.tarif.get_taxe_price(),
            APassenger.DEVISE: self.tarif.get_device(),
            Passenger.CHILD: self.tarif.get_child_unit_price(),
            Passenger.ADULT: self.tarif.get_adult_unit_price(),
            Passenger.BABY: self.tarif.get_inf_unit_price()
        }

    def passengers_infos(self, reservation) -> Any:
        return self.queryset().filter(journey=reservation)\
            .annotate(**self.anotate())


@dataclass
class ReservationQuery:
    """ all queryset and model process"""
    related = (
        "journey",
        "journey__route__node",
        "journey__route__origin__node",
        "session",
        "journey_class",
        "other_info",
    )
    prefetch = ()

    # passengers queries
    passengers: PassengersQueries
    tarif: PriceSelectorProtocol
    queryset: models.QuerySet[Reservation]
    reservation: Reservation = field(init=False)

    def get_reservation(self, session: Optional[str] = None):
        self.reservation = self.get_queryset().get(session__key=session)
        return self.reservation

    def get_queryset(self):
        return self.queryset.select_related(*self.related)\
            .prefetch_related(*self.prefetch)\
            .annotate(**self.annotate())

    def annotate(self) -> dict:
        return OrderedDict(
            devise=self.tarif.get_device(),
            taxe=self.tarif.get_taxe_price(),
            adult_price=self.tarif.get_adult_unit_price(),
            inf_price=self.tarif.get_inf_unit_price(),
            child_price=self.tarif.get_child_unit_price()
        )

    def get_passengers(self) -> list:
        """ list of passengers of reservations."""
        return self.passengers.passengers_infos(reservation=self.reservation)
        # if (
        #     hasattr(self.reservation, "passengers") and
        #     hasattr(self.reservation.passengers,
        #             "select_related")  # type: ignore
        # ):
        #     # type: ignore
        #     return self.reservation.passengers.select_related("passenger_ticket")
        # return []

    def get_other_info(self) -> Optional[OtherInfoReservation]:
        with contextlib.suppress(OtherInfoReservation.DoesNotExist):
            if hasattr(self.reservation, "other_info"):
                return self.reservation.other_info  # type: ignore

    def get_journey(self) -> Optional[Journey]:
        return self.reservation.journey

    def get_session(self) -> c_models.JourneySession:
        return self.reservation.session


@dataclass
class InfoReservation:
    queryset: ReservationQuery
    price_sys: IPriceSystem
    ticket_sender: TicketSender
    title_fullname: TitleFullname = str_system.title_fullname
    session: str = field(init=False)
    error: Union[str, None] = field(init=False)

    @property
    def reservation(self):
        return self.queryset.reservation

    def is_valide(self, session: Optional[str] = None) -> bool:
        with contextlib.suppress(Reservation.DoesNotExist):
            reservation = self.queryset.get_reservation(session=session)

            # set passengers number...
            self.price_sys.set_passenger(
                adult=reservation.adult,
                child=reservation.child,
                inf=reservation.baby,
            )

            # set tarif value
            self.price_sys.set_tarif(
                taxe=reservation.taxe,  # type: ignore
                adult_price=reservation.adult_price,  # type: ignore
                child_price=reservation.child_price,  # type: ignore
                inf_price=reservation.inf_price  # type: ignore
            )

            return True
        self.error = SESSION_INVALID
        return False

    def reservation_progression(self):
        """return the progression of reservation"""
        progression = self.queryset.reservation
        return Progression(
            adult=progression.adult,
            child=progression.child,
            inf=progression.baby,
            step=progression.step,
            passengers=self.queryset.get_passengers()
        )

    def info_journey_message(self) -> str:
        if info := self.queryset.get_journey():
            objt = OrderedDict(
                j_number=info.numJourney,
                where_from=info.route.origin.node.town,  # type: ignore
                where_to=info.route.node.town,  # type: ignore
                d_where_from=str_system.stringfy_datetime(
                    info.dateDeparture),  # type: ignore
                h_where_from=str_system.stringfy_datetime(
                    info.hoursDeparture, str_system.TIME_FORMAT),  # type: ignore
                w_where_to=str_system.stringfy_datetime(
                    info.hoursReturn, str_system.TIME_FORMAT),  # type: ignore
                d_where_to=str_system.stringfy_datetime(
                    info.dateReturn)  # type: ignore
            )
            return InfoJourneyMessage.get_info_message(**objt)
        return "-"

    def booker(self) -> str:
        """ fullname of booker """
        if other_info := self.queryset.get_other_info():
            return self.title_fullname(
                gender=other_info.gender or "",
                fullname=other_info.fullname
            )
        return "-"

    def get_devise(self) -> str:
        return self.reservation.devise if hasattr(  # type: ignore
            self.reservation, "devise") else "USD"

    def total_price(self) -> str:
        """ return a total of price """
        device = self.get_devise()
        total_price = self.price_sys.get_total_price()
        return f"{total_price} {device}"

    def reservation_completed(self):
        """
        booker: str,
        expire_datetime: Date,
        pnr: str,
        total_price: 20000 Fc,
        text_reservation:str
        passengers: str[]
        """
        session = self.queryset.get_session()
        tmp_passengers = self.queryset.get_passengers()
        passengers: List[str] = [
            self.title_fullname(
                gender=passenger.gender,
                fullname=passenger.fullname
            ) for passenger in tmp_passengers
        ]

        return OrderedDict(
            booker=self.booker(),
            total_price=self.total_price(),
            text_reservation=self.info_journey_message(),
            expire_datetime=session.date_expiration,
            pnr=self.reservation.pnr,
            passengers=passengers,
        )
        # self.send_ticket(to=self.reservation.other_info.email)
        # return completed

    def send_ticket(self, *args, **kwargs):
        """ sending ticket to booker"""
        self.ticket_sender.send_ticket(*args, **kwargs)


@dataclass
class InfoReservationInterface:
    reservation: InfoReservation

    def mixin_reservation(self, session: str, callback: Callable[[], Any]) -> RETURN_TYPE:
        if self.reservation.is_valide(session=session):
            return True, callback()
        return False, self.reservation.error or SESSION_INVALID

    def progression(self, session: str) -> RETURN_TYPE:
        return self.mixin_reservation(
            session=session,
            callback=self.reservation.reservation_progression
        )

    def completed(self, session: str) -> RETURN_TYPE:
        return self.mixin_reservation(
            session=session,
            callback=self.reservation.reservation_completed
        )


apis_info = InfoReservationInterface(
    reservation=InfoReservation(
        ticket_sender=SendTicket,
        price_sys=PriceSystem(),
        queryset=ReservationQuery(
            passengers=PassengersQueries(
                tarif=PriceSelector(
                    queryset=JourneyTarif.objects.filter(
                        route=models.OuterRef("journey__journey__route")
                    )
                )
            ),
            queryset=Reservation.objects.all(),
            tarif=PriceSelector(
                queryset=JourneyTarif.objects.filter(
                    route=models.OuterRef("journey__route")
                )
            )
        )
    )
)
