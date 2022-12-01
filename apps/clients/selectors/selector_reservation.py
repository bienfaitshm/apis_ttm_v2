from typing import Any, Dict, List, Optional, TypedDict

from django.conf import settings
from django.db import models
from django.db.models.functions import Concat
from django.utils import timezone
from fuzzywuzzy import fuzz

from apps.clients import models as client_model
from apps.clients.data_type import RJourneyDataType
from apps.clients.selectors import search
from apps.dash import models as dash_model
from apps.dash.services import routes_service

from ..models import Passenger, Reservation

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


class JourniesService:
    queryset = dash_model.Journey.objects.exclude(
        route=None
    ).select_related("route")

    def get_queryset(self):
        return self.queryset

    def get_journies(self):
        return dash_model.Journey.objects.exclude(
            route=None
        ).select_related("route")


class SearchJourneyService:
    class_name: str = "mique"
    tarifs: Dict[str, Dict[str, Any]] = {}

    def list(self):
        self.convert_tarif_2_dict()
        self.search_class_name()
        route = self.get_routes()
        routes_service.recursive()
        print(self.tarifs)
        print("\n\n routes ===>\n\n", route)
        return []

    def search_class_name(self):
        for key, value in self.tarifs.items():
            poids = fuzz.ratio(self.class_name, value.get("j_class"))
            value["cls_name_weith"] = poids

    def convert_tarif_2_dict(self, *args, **kwargs):
        items = self.get_total_tarif(*args, **kwargs)
        for item in items:
            self.tarifs[item.get("route", "none")] = item

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def f_total_price(self, adult: int = 1, child: int = 0, inf: int = 0):
        return (
            models.F("tp_ad") * adult
        ) + (models.F("tp_chd") * child) + (models.F("tp_inf") * inf)

    def get_journies(self):
        return dash_model.Journey.objects.exclude(
            route=None
        ).select_related("route")

    def get_total_tarif(self, *args, **kwargs):
        return self.get_tarif().annotate(
            total_price=self.f_total_price(*args, **kwargs)
        ).values("devise", "route", "j_class", "j_class_id", "total_price")

    def get_tarif(self):
        route_ids = self.get_journies().values_list("route", flat=True)
        return dash_model.JourneyTarif.objects.filter(
            route__in=route_ids,
            actif=True
        ).select_related("journey_class").annotate(
            j_class=models.F("journey_class__name"),
            j_class_id=models.F("journey_class_id"),
            tp_ad=self.ptt(),
            tp_chd=self.ptt("child"),
            tp_inf=self.ptt("baby")
        )

    def get_routes(self):
        return dash_model.Routing.objects.all().select_related("node")


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
    # tarifs = tarif_2_dict_values()
    journies = journey_2_list_values()
    print("journies ", journies)
    return datas


def find_reservation_journey() -> List[RJourneyDataType]:
    data: List[RJourneyDataType] = fake_data
    data_pr = SearchJourneyService()
    data_pr.list()
    return data


def get_dash_reservations():
    return Reservation.objects.all()


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

    return Reservation.objects\
        .select_related(*select_related)\
        .prefetch_related(*prefetch_related)\
        .annotate(
            client_full_name=client_full_name,
            n_folder=models.F("folder__number")
        )
