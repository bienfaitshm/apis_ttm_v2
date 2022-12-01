import contextlib

from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import (
    Any, Callable, List, Literal, Optional, Protocol, Tuple, Union,
)

from django.conf import settings
from django.db.models import QuerySet

from apps.clients.models import (
    JourneySession, OtherInfoReservation, Passenger, Reservation,
)
from apps.dash.models import Journey
from systen.send_ticket import SendEmailReservation
from utils.times import get_date_expiration

from .utils import (
    TNTypeUser, clone_value, combiner_datetime, key_session_creator,
    nps_by_type, pnr_creator,
)

# Type list of passengers
TLPassenger = Union[List[int], List[Passenger]]
TFromDate = Optional[Callable[[], datetime]]
TTReturn = Tuple[Union[Literal[False], Literal[True]], Any]


class NumberOfPassengersByType(Protocol):
    def __call__(self, passengers: List[Passenger]) -> TNTypeUser: ...


class StringCreator(Protocol):
    def __call__(self, *args, **kwargs) -> str: ...


class DateCombinator(Protocol):
    def __call__(self, date: date, time: time) -> datetime: ...


class ExpireDateSession(Protocol):
    def __call__(self,
                 date_dep: datetime,
                 from_date: TFromDate = None, *args, **kwargs) -> Any: ...


class ClonerValue(Protocol):
    def __call__(self, obj: Any, addons: Optional[dict] = None) -> dict: ...


class TicketCreator(Protocol):
    def create_ticket(self, *args, **kwargs): ...


class SendEmailReservation(Protocol):
    def send_email(self, *args, **kwargs) -> Any: ...


class IQueryReservation(Protocol):
    def reserve(
        self, journey: Union[Journey, int], *args, **kwargs): ...

    def get_reservation(self, *args, **kwargs): ...
    def get_passengers(self, *args, **kwargs) -> QuerySet[Passenger]: ...
    def passengers(self, *args, **kwargs) -> TTReturn: ...
    def other_info(self, *args, **kwargs) -> TTReturn: ...


@dataclass
class ReservationQuery(IQueryReservation):
    # models
    reservation_model = Reservation
    passengers_model = Passenger
    session_model = JourneySession
    other_info_model = OtherInfoReservation
    # addons
    pnr_creator: StringCreator
    key_creator: StringCreator
    cloner: ClonerValue
    date_exp_creator: ExpireDateSession
    combiner_datetime: DateCombinator

    def _filter_dict(self, *args, **kwargs) -> dict:

        reservation = kwargs.get("reservation")
        _filter = OrderedDict()
        if isinstance(reservation, (str, int)):
            _filter["pk"] = kwargs.get("reservation")
        if "session" in kwargs:
            _filter["session__key"] = kwargs.get("session")
        return _filter

    def get_reservation(self, *args, **kwargs) -> Optional[reservation_model]:
        """return the reservation"""
        reservation = kwargs.get("reservation")
        if isinstance(reservation, self. reservation_model):
            return reservation

        with contextlib.suppress(self. reservation_model.DoesNotExist):
            return self. reservation_model.objects.select_related("session")\
                .get(**self._filter_dict(*args, **kwargs))

    def create_reservation(self, journey: Any,
                           session: Any,
                           pnr: Any, *args, **kwargs) -> Reservation:
        """creation of data reservation"""
        return Reservation.objects.create(
            session=session,
            journey=journey,
            pnr=pnr, *args, **kwargs)

    def get_passengers(self, *args, **kwargs):
        """return list of passengers"""
        passengers: TLPassenger = kwargs.get("passengers", [])

        # ids for passangers
        passengers_ids = [
            passenger.pk if isinstance(
                passenger, self.passengers_model) else passenger
            for passenger in passengers]

        return self.passengers_model.objects.filter(pk__in=passengers_ids)

    def create_session(self, date_dep):
        """create nez session """
        date_exp = self.date_exp_creator(date_dep=date_dep, from_date=None)
        key = self.key_creator()
        return self.session_model.objects.create(
            key=key,
            date_expiration=date_exp
        )

    def reserve(self, journey: Journey, *args, **kwargs):
        """create a new reservation"""
        date_dep = self.combiner_datetime(
            date=journey.dateDeparture,
            time=journey.hoursDeparture
        )
        session = self.create_session(date_dep)
        return self.create_reservation(
            journey=journey,
            session=session,
            pnr=self.pnr_creator(),
            *args, **kwargs
        )

    def passengers(self, journey: Journey, psg: Optional[Any] = None, ) -> TTReturn:
        """Creating reservation of passengers"""
        if psg is None:
            psg = []
        self.passengers_model.objects.bulk_create([
            self.passengers_model(**i, journey=journey) for i in psg
        ])
        return True, OrderedDict(
            passengers=self.passengers_model.objects.filter(journey=journey),
            reservation=journey
        )

    def other_info(self, journey: Journey, *args, **kwargs) -> TTReturn:
        """adding creating other info"""
        other_info = self.other_info_model.objects.filter(journey=journey)
        return (False, other_info.first()) if other_info.exists() else (True, self.other_info_model.objects.create(*args, **kwargs))


@dataclass
class RootReservation:
    pnr_creator: StringCreator
    query: IQueryReservation
    send_email: SendEmailReservation

    def reserve(self, *args, **kwargs):
        if journey := kwargs.get("journey"):
            return True, self.query.reserve(journey=journey)
        return False, "Not Reservation selected, Please try again"

    def passengers(self, *args, **kwargs):
        return self.query.passengers(*args, **kwargs)

    def other_info(self, *args, **kwargs):
        created, value = self.query.other_info(*args, **kwargs)
        if created:
            self.send_email.send_email(value=value)
        return True, value


@dataclass
class ActionReservation:
    res_field_name = "reservation"
    number_by_type_of_user: NumberOfPassengersByType
    query: IQueryReservation

    def void(self, *args, **kwargs) -> bool:
        """ void a reservation"""
        reservation = kwargs.get(self.res_field_name)
        if isinstance(reservation, (int, str)):
            return Reservation.objects\
                .filter(pk=reservation)\
                .update(status=Reservation.VOIDED) == 1

        if isinstance(reservation, Reservation):
            reservation.status = Reservation.VOIDED
            reservation.save()
            return True
        return False

    def splite(self, *args, **kwargs) -> tuple:
        query_reservation = self.query.get_reservation(*args, **kwargs)
        query_passengers = self.query.get_passengers(*args, **kwargs)

        if query_reservation is None:
            return False, "not reservation have this key"

        # default number of passengers not allowed
        nps_not_allowed: int = query_passengers\
            .exclude(journey=query_reservation).count()

        if nps_not_allowed > 0:
            return False, "same passengers dosent have this reservation"

        return False, "error"


@dataclass
class ReservationApisService:
    actions: ActionReservation
    root: RootReservation

    def reserve(self, *args, **kwargs):
        return self.root.reserve(*args, **kwargs)

    def passengers(self, *args, **kwargs):
        return self.root.passengers(*args, **kwargs)

    def other_info(self, *args, **kwargs):
        return self.root.other_info(*args, **kwargs)

    def void(self, *args, **kwargs):
        return self.actions.void(*args, **kwargs)

    def splite(self, *args, **kwargs):
        return self.actions.splite(*args, **kwargs)


query_res = ReservationQuery(
    pnr_creator=pnr_creator,
    key_creator=key_session_creator,
    date_exp_creator=get_date_expiration,
    combiner_datetime=combiner_datetime,
    cloner=clone_value
)

reservation_apis_service = ReservationApisService(
    actions=ActionReservation(
        query=query_res,
        number_by_type_of_user=nps_by_type
    ),
    root=RootReservation(
        send_email=SendEmailReservation,
        pnr_creator=pnr_creator,
        query=query_res,
    )
)
