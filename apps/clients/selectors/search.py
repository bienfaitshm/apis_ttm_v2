from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import Any, List, Optional, TypedDict, Union

from django.db import models
from django.db.models import OuterRef, Subquery

from apps.dash.models import Journey, JourneyTarif, managers
from apps.dash.services.routes import Routes

JOURNEY_ORDERD = deque[Journey]


class JourneyAnotationDictType(TypedDict):
    where_to: Any
    where_from: Any
    cls_name: Any
    cls_id: Any
    total_price: Optional[Any]


def initial_value() -> JOURNEY_ORDERD:
    return deque([])


@dataclass
class ClsSelector:
    cls_field = "journey_class"
    cls_field_name = f"{cls_field}__name"
    cls_join = (cls_field_name,)

    @property
    def query(self):
        return JourneyTarif.objects.filter(
            route=OuterRef("route")
        )

    @property
    def get_cls_name(self):
        return Subquery(
            queryset=self.query.select_related(*self.cls_join).annotate(
                cls_name=models.F(self.cls_field)
            ).values("cls_name"),
            output_field=models.CharField()
        )

    @property
    def get_cls_id(self):
        return Subquery(
            queryset=self.query.values(self.cls_field),
            output_field=models.IntegerField()
        )


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
        return self.route_join

    @property
    def sync_route(self) -> None:
        self.route_services.sync()

    def get_scales(self, origin: Union[str, int]) -> List[str]:
        scales = self.route_services.get_scales_in_ordered(origin)
        return [i.town for i in scales]


@dataclass
class PriceSelector:
    query: models.QuerySet[JourneyTarif]

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def f_total_price(self, adult: int = 1, child: int = 0, inf: int = 0):
        return (
            models.F("tp_ad") * adult
        ) + (models.F("tp_chd") * child) + (models.F("tp_inf") * inf)

    def get_total_price(self, *args, **kwargs):
        return Subquery(
            queryset=self.query.annotate(
                tp_ad=self.ptt(),
                tp_chd=self.ptt("child"),
                tp_inf=self.ptt("baby")
            ).annotate(
                total_price=self.f_total_price(*args, **kwargs)
            ).values("total_price"),
            output_field=models.FloatField()
        )


@dataclass
class PassengerSelector:
    pass


@dataclass
class JourneySelector:
    cls_selector: ClsSelector
    route_selector: RouteSelector
    query: managers.JourneyManager
    price_selector: PriceSelector
    journies: JOURNEY_ORDERD = field(
        init=False,
        default_factory=initial_value
    )

    def get_annotate(self) -> JourneyAnotationDictType:
        return {
            "total_price": self.price_selector.get_total_price(),
            "cls_id": self.cls_selector.get_cls_id,
            "cls_name": self.cls_selector.get_cls_name,
            "where_to": models.F("route__node__town"),
            "where_from": models.F("route__origin__node__town"),
        }

    def get_queryset(self):
        route_join = self.route_selector.get_route_join
        return self.query.select_related(*route_join).annotate(**self.get_annotate())

    def get_journies(self):
        return self.get_queryset()


@dataclass
class SearchSelector:
    pass


def search_selector(manager: managers.JourneyManager, *args, **kwargs):
    cls_selector = ClsSelector()
    svc_route = Routes()
    price_selector = PriceSelector(query=cls_selector.query)
    route_selector = RouteSelector(route_services=svc_route)
    jouries = JourneySelector(
        query=manager,
        cls_selector=cls_selector,
        route_selector=route_selector,
        price_selector=price_selector
    )
    return jouries.get_journies()
