import string

from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from django.db.models import Count, QuerySet
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.clients import data_type as dtype, models as client_model
from apps.clients.message import ErrorMessage
from apps.dash.models.transport import Journey
from utils.times import get_date_expiration

from ..models import (
    JourneyClientFolder, JourneySession, OtherInfoReservation, Passenger,
    SeletectedJourney as Reservation,
)
from .exceptions import MessageExpection

QueryReservationType = QuerySet[Reservation]
SpliteTypeReturn = Union[Tuple[Literal["error"], str],
                         Tuple[Literal["success"], QueryReservationType]]
TypeReservationParams = Union[int, QueryReservationType]


def clone_and_value(obj, addons=None):
    """Returns a clone of this instance."""
    if addons is None:
        addons = {}
    data = {f.attname: getattr(obj, f.attname)
            for f in obj.__class__._meta.fields}
    return {**data, **addons}


def _get_radom_string():
    return get_random_string(20, string.ascii_letters)


def _get_number_type_user(passengers: list[Passenger]) -> Dict[str, int]:
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


def create_pnr():
    """create png function"""
    return get_random_string(6, string.ascii_uppercase)


def create_data_reservation(
        journey: Any,
        session: Any,
        folder: Any,
        pnr: Any, *args, **kwargs) -> Reservation:
    """creation of data reservation"""
    return Reservation.objects.create(
        session=session,
        journey=journey,
        folder=folder,
        pnr=pnr, *args, **kwargs)


def create_reservation(journey: Journey, *args, **kwargs):
    date_dep = datetime.now()  # default time...
    # get time of expiration of journey
    if isinstance(journey, Journey):
        date_dep = datetime.combine(
            date=journey.dateDeparture,
            time=journey.hoursDeparture
        )

    session = create_session(date_dep)
    folder = create_folder()
    pnr = create_pnr()
    return create_data_reservation(
        journey=journey, session=session,
        pnr=pnr, folder=folder, *args, **kwargs)


def create_session(
        date_dep: Any = None,
        get_key_creator: Callable[[], str] = _get_radom_string,
        get_data_creator: Callable[[Any], Any] = get_date_expiration
) -> JourneySession:
    """ session creator """
    date_exp = get_data_creator(date_dep)
    key = get_key_creator()

    return JourneySession.objects.create(
        key=key, date_expiration=date_exp
    )


def create_folder():
    return JourneyClientFolder.objects.create(
        number=get_random_string(6, string.digits),
        session=get_random_string(5, string.ascii_letters)
    )


def splite_reservation(
    reservation: Union[int, Reservation],
    passengers: Union[List[int], List[Passenger]]
) -> Union[SpliteTypeReturn, None]:
    passengers_notallowed: int = 0

    if isinstance(reservation, int):
        reservation = Reservation.objects.select_related(
            "session"
        ).get(pk=reservation)

    passengers_ids = [
        passenger.pk if isinstance(passenger, Passenger) else passenger
        for passenger in passengers]

    passengers_in = Passenger.objects.filter(pk__in=passengers_ids)
    passengers_notallowed = passengers_in.exclude(journey=reservation).count()
    d = passengers_in.values("typeUser").annotate(total=Count("typeUser"))

    print(d)

    if passengers_notallowed > 0:
        return "error", MessageExpection.PASSENGERS_NO_ALLOWED

    if isinstance(reservation, Reservation):
        if reservation.status == Reservation.VOIDED:
            return "error", MessageExpection.VOID_NO_ALLOWED

        n_pnr = create_pnr()
        n_passengers = _get_number_type_user(passengers)  # type: ignore

        new_session = create_session(
            get_data_creator=lambda _: reservation.session.date_expiration)

        new_reservation_data = clone_and_value(
            reservation, {
                "id": None,
                "session_id": new_session.pk, ** n_passengers, "pnr": n_pnr})

        new_reservation = Reservation.objects.create(
            **new_reservation_data)

        if hasattr(reservation, "other_info"):
            other_info = reservation.other_info  # type: ignore
            new_data_other_info = clone_and_value(other_info)
            new_data_other_info.pop("journey_id")
            new_data_other_info.pop("id")
            add_other_info(new_reservation, new_data_other_info)

        if passengers_in.update(journey=new_reservation):
            return "success", new_reservation

    return "error", MessageExpection.IMPOSSIBLE


def add_other_info(*args, **kwargs):
    journey = kwargs.get("journey")
    if not journey:
        return False, ErrorMessage

    other_info = OtherInfoReservation.objects.filter(
        journey=journey
    )

    return (
        True, other_info.first()
    ) if other_info.exists() else (
        True, OtherInfoReservation.objects.create(*args, **kwargs)
    )


def add_passengers(*args, **kwargs):
    journey = kwargs.get("journey")
    passengers: list = kwargs.get("passengers", [])

    if not journey:
        return False, ErrorMessage

    Passenger.objects.bulk_create([
        Passenger(**i, journey=journey) for i in passengers
    ])

    return True, Passenger.objects.filter(journey=journey)

# bmpkcvvnrsgtvxsa


class ReservationServices:
    pnr_creator: Callable[[], str] = create_pnr
    key_creator: Callable[[], str] = _get_radom_string
    date_expire_creator: Callable[[Any], Any] = get_date_expiration

    def __init__(self, session):
        self.session = session

    def get_journey(self):
        return self.session

    def get_creator_pnr(self):
        return self.pnr_creator()

    def set_pnr_creator(self, pnr_creator: Callable[[], str]):
        self.pnr_creator = pnr_creator

    def set_key_creator(self, key_creator: Callable[[], str]):
        self.key_creator = key_creator

    def set_date_expire_creator(
        self,
        date_expire_creator: Callable[[Any], Any]
    ):
        self.date_expire_creator = date_expire_creator

    def get_completed(self, ) -> dtype.RCompletedDataType:
        return {
            "booker": "Mr bienfait kilumba shomari",
            "expire_datetime": datetime.now(),
            "pnr": "YYTRE345",
            "text_reservation":
                "voyage No 2345, likashi-kolwezi, depart mardi 12/02/2002 a 12h20; arrive mardi mardi 12/02/2002 a 12h20",
            "total_price": "20000 Fc",
            "passengers": [
                "Mr kilumba shomari",
                "Mm prisca kilumba zSUvIThLwfHIcmpMbwfU",
            ],
        }

    def passengers(self, psg=None):
        if psg is None:
            psg = []
        journey = self.get_journey()
        client_model.Passenger.objects.bulk_create([
            client_model.Passenger(**i, journey=journey) for i in psg
        ])

        return True, client_model.Passenger.objects.filter(journey=journey)

    def tickets(self, status, passengers: list = [], ):
        pass

    def other_info(self, *args, **kwargs):
        journey = self.get_journey()
        other_info = client_model.OtherInfoReservation.objects.filter(
            journey=journey
        )
        if other_info.first():
            return True, client_model.OtherInfoReservation.objects.create(
                *args, **kwargs
            )
        return True, other_info.first()

    def create_reservation(
        self,
        journey,
        j_cls,
        adult,
        child,
        baby,
        pnr_creator: Callable[[], str] = create_pnr
    ):
        if pnr_creator and journey:
            pnr = pnr_creator()
            session = self.create_session(date_dep=journey.datetime_from)
            select = client_model.SeletectedJourney.objects.create(
                pnr=pnr,
                session=session,
                journey_class=j_cls,
                adult=adult,
                child=child,
                baby=baby,
                journey=journey
            )
            return True, select
        return False, "Il semble qu'il ya eu erreur"

    def create_session(
        self,
        date_dep: Any = None,
        get_key_creator: Callable[[], str] = _get_radom_string,
        get_date_creator: Callable[[Any], Any] = get_date_expiration
    ) -> JourneySession:
        """ session creator """
        date_exp = get_date_creator(date_dep)
        key = get_key_creator()
        return client_model.JourneySession.objects.create(
            key=key,
            date_expiration=date_exp
        )


class ReservationActionService:
    pass


def void_reservation(reservation: Union[Reservation, int]) -> int:
    if isinstance(reservation, (int, str)):
        return Reservation.objects.filter(
            pk=reservation).update(status=Reservation.VOIDED)

    if isinstance(reservation, Reservation):
        reservation.status = Reservation.VOIDED
        reservation.save()
        return True
    return False
