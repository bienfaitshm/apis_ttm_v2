from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import List, Union

from django.db import models
from django.db.models import OuterRef, Subquery

from apps.dash.models import Journey, JourneyTarif, managers
from apps.dash.services.routes import Routes

JOURNEY_ORDERD = deque[Journey]


def initial_value() -> JOURNEY_ORDERD:
    return deque([])


@dataclass
class RouteSelector:
    route_services: Routes
    route_join = (
        "route",
        "route__node",
        "route__origin__node",
    )

    @property
    def get_route_join(self):
        return self.get_route_join

    @property
    def sync_route(self) -> None:
        self.route_services.sync()

    def get_scales(self, origin: Union[str, int]) -> List[str]:
        scales = self.route_services.get_scales_in_ordered(origin)
        return [i.town for i in scales]


@dataclass
class JourneySelector:
    pass


@dataclass
class SearchSelector:
    j_manager: managers.JourneyManager
    ordered_data: JOURNEY_ORDERD = field(
        init=False,
        default_factory=initial_value
    )

    root_join = (
        "route",
        "route__node",
        "route__origin__node",
    )

    def get_journies(self) -> JOURNEY_ORDERD:
        _data = self.get_search()
        for item in _data:
            self.ordered_data.append(item)
        return self.ordered_data

    def get_anotation(self) -> dict:
        return {
            "where_to": models.F("route__node__town"),
            "where_from": models.F("route__origin__node__town"),
            "cls_name": self.get_cls_name,
            "cls_id": self.get_cls_id,
            "total_price": self.get_total_price()
        }

    def get_search(self):
        return self.j_manager.select_related(*self.root_join).annotate(
            **self.get_anotation()
        )

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def f_total_price(self, adult: int = 1, child: int = 0, inf: int = 0):
        return (
            models.F("tp_ad") * adult
        ) + (models.F("tp_chd") * child) + (models.F("tp_inf") * inf)

    def get_total_price(self, *args, **kwargs):
        return Subquery(
            queryset=self.get_cls().annotate(
                tp_ad=self.ptt(),
                tp_chd=self.ptt("child"),
                tp_inf=self.ptt("baby")
            ).annotate(
                total_price=self.f_total_price(*args, **kwargs)
            ).values("total_price"),
            output_field=models.FloatField()
        )

    def get_cls(self):
        return JourneyTarif.objects.filter(
            route=OuterRef("route")
        )

    @property
    def get_cls_name(self):
        return Subquery(
            queryset=self.get_cls().select_related("journey_class").annotate(
                cls_name=models.F("journey_class__name")
            ).values("cls_name"),
            output_field=models.CharField()
        )

    @property
    def get_cls_id(self):
        return Subquery(
            queryset=self.get_cls().values("journey_class"),
            output_field=models.IntegerField()
        )
