import string

from datetime import datetime
from typing import Any, Callable, Dict, List, Literal, Tuple, Union

from django.db.models import Count, QuerySet
from django.utils.crypto import get_random_string

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


def add_other_info(
        journey: Any,
        other_info: Any
) -> Union[OtherInfoReservation, None]:
    existing_other_info = OtherInfoReservation.objects.filter(
        journey=journey)
    if not existing_other_info.exists():
        return OtherInfoReservation.objects.create(
            journey=journey, **other_info
        )
    return existing_other_info.first()


def add_passengers(jouney: Any, passengers: List[Any]) -> QuerySet[Passenger]:
    Passenger.objects.bulk_create([
        Passenger(**i, journey=jouney) for i in passengers
    ])

    return Passenger.objects.filter(journey=jouney)


def void_reservation(reservation: Union[Reservation, int]) -> int:
    if isinstance(reservation, (int, str)):
        return Reservation.objects.filter(
            pk=reservation).update(status=Reservation.VOIDED)

    if isinstance(reservation, Reservation):
        reservation.status = Reservation.VOIDED
        reservation.save()
        return True
    return False
