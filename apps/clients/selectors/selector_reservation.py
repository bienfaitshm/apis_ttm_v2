from typing import Any, Dict, List, Optional, TypedDict

from django.conf import settings
from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone

from apps.dash import models as dash_model

from ..models import Passenger, SeletectedJourney


class RJourneyDataType(TypedDict):
    uid: int
    where_from: str
    where_to: str
    datetime_from: Any
    datetime_to: Any
    duration: Any
    j_class: str
    total_price: int
    device: str
    has_ascale: bool
    passengers: Optional[Any]
    scales: Optional[List[str]]
    message: Optional[str]
    is_selected_for: Optional[bool]
    is_expired: Optional[bool]


fake_data: List[RJourneyDataType] = [
    {
        "uid": 0,
        "where_from": "Lubumbash",
        "where_to": "Dilolo",
        "datetime_from": timezone.now(),
        "datetime_to": timezone.now(),
        "duration": timezone.now(),
        "j_class": "Ecolo",
        "total_price": 90,
        "device": "CDF",
        "has_ascale": False,
        "scales": [],
        "is_expired":False,
        "is_selected_for":False,
        "message":"selection pour vous",
        "passengers":{
            "adult": 3,
            "inf": 0,
            "child": 0
        }
    },
    {
        "uid": 1,
        "where_from": "Lubumbash",
        "where_to": "Dilolo",
        "datetime_from": timezone.now(),
        "datetime_to": timezone.now(),
        "duration": timezone.now(),
        "j_class": "Ecolo",
        "total_price": 923,
        "device": "CDF",
        "has_ascale": False,
        "scales": [],
        "is_expired":False,
        "is_selected_for":False,
        "message":"selection pour vous",
        "passengers":{
            "adult": 3,
            "inf": 0,
            "child": 0
        }
    },
    {
        "uid": 1,
        "where_from": "Lubumbash",
        "where_to": "Dilolo",
        "datetime_from": timezone.now(),
        "datetime_to": timezone.now(),
        "duration": timezone.now(),
        "j_class": "Ecolo",
        "total_price": 923,
        "device": "CDF",
        "has_ascale": True,
        "scales": ["Dilolo", "Kambove"],
        "is_expired":True,
        "is_selected_for":True,
        "message":"selection pour vous",
        "passengers":{
            "adult": 3,
            "inf": 3,
            "child": 0
        }
    },
]


def tarif_2_dict_values(*args, **kwargs):
    tarifs = dash_model.JourneyTarif.objects.filter(
        actif=True, *args, **kwargs
    ).select_related("route", "journey_class")\
        .annotate(j_class=models.F("journey_class__name"))\
        .values("j_class", "adult", "child", "baby", "taxe", "route")

    return {item.get("route"): item for item in tarifs}  # type: ignore


def journey_2_list_values(*args, **kwargs):
    journies = dash_model.Journey.objects.all()\
        .select_related("route", "route__origin")\
        .annotate(
        where_to=models.F("route__node__town")
    )
    return journies.values("where_to")


def data_process():
    datas = []
    tarifs = tarif_2_dict_values()
    journies = journey_2_list_values()
    print("journies ", journies)
    return datas


def find_reservation_journey() -> List[RJourneyDataType]:
    data: List[RJourneyDataType] = fake_data
    data_pr = data_process()
    return data


def get_dash_reservations():
    return SeletectedJourney.objects.all()


def get_dash_detail_reservation():
    select_related = ("other_info", "journey", "journey_class",)
    prefetch_related = ("passengers",)

    client_full_name = models.ExpressionWrapper(
        Concat(
            models.F("other_info__firstname"),
            models.Value(" "),
            models.F("other_info__middlename"),
            models.Value(" "),
            models.F("other_info__lastname"),
        ),
        output_field=models.CharField(max_length=200)
    )

    return SeletectedJourney.objects\
        .select_related(*select_related)\
        .prefetch_related(*prefetch_related)\
        .annotate(
            client_full_name=client_full_name,
            n_folder=models.F("folder__number")
        )
