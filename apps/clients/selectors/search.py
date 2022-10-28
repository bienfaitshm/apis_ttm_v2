from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import Any, List, Optional, TypedDict, Union

from django.db import models
from django.db.models import OuterRef, Subquery

from apps.dash.models import Journey, JourneyTarif, managers
from apps.dash.services.routes import Routes

JOURNEY_ORDERD = deque[Journey]
INT_STR = Union[str, int]
# query string
ADULT_PARAMS = "adult"
CHILD_PARAMS = "child"
INF_PARAMS = "baby"
DATE_DEPARTURE_PARAMS = "dateDepature"
CLS_NAME_PARAMS = "journeyClass"
WHERE_FROM_PARAMS = "whereFrom"
WHERE_TO_PARAMS = "whereTo"


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
                cls_name=models.F(self.cls_field_name)
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
        "route__origin",
        "route__origin__node",
    )

    @property
    def get_route_join(self):
        return self.route_join

    def sync_route(self) -> None:
        self.route_services.sync()

    def get_scales(self, origin: Union[str, int]) -> List[str]:
        scales = self.route_services.get_scales_in_ordered(origin)
        return [i.node.town for i in scales]


@dataclass
class PriceSelector:
    query: models.QuerySet[JourneyTarif]
    adult: int = 3
    child: int = 2
    inf: int = 1

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def f_total_price(self):
        return (
            models.F("tp_ad") * self.adult
        ) + (models.F("tp_chd") * self.child) + (models.F("tp_inf") * self.inf)

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

    @property
    def passengers(self):
        return OrderedDict(adult=self.adult, child=self.child, inf=self.inf)

    def parse_int(self, value: INT_STR, default: int = 0) -> int:
        if isinstance(value, int):
            return value
        return int(value) if isinstance(value, str) and value.isdigit() else default

    def set_adult(self, adult: INT_STR):
        self.adult = self.parse_int(adult, self.adult)

    def set_child(self, child: INT_STR):
        self.child = self.parse_int(child, self.child)

    def set_inf(self, inf: INT_STR):
        self.inf = self.parse_int(inf, self.inf)


@dataclass
class SearchSelector:
    cls_selector: ClsSelector
    route_selector: RouteSelector
    price_selector: PriceSelector

    def get_route_join(self):
        return self.route_selector.get_route_join

    def sync_route(self):
        self.route_selector.sync_route()

    def get_total_price(self):
        return self.price_selector.get_total_price()

    def cls_id(self):
        return self.cls_selector.get_cls_id

    def cls_name(self):
        return self.cls_selector.get_cls_name

    def passengers(self):
        return self.price_selector.passengers

    def get_scales(self, item: Any):
        return self.route_selector.get_scales(item)

    def request(self, *args, **kwargs):
        if adult := kwargs.get(ADULT_PARAMS):
            self.price_selector.set_adult(get_params_value(adult))
        if child := kwargs.get(CHILD_PARAMS):
            self.price_selector.set_child(get_params_value(child))
        if inf := kwargs.get(INF_PARAMS):
            self.price_selector.set_inf(get_params_value(inf))


@dataclass
class JourneySelector:
    search_selector: SearchSelector
    query: managers.JourneyManager
    journies: JOURNEY_ORDERD = field(
        init=False,
        default_factory=initial_value
    )

    def get_annotate(self) -> JourneyAnotationDictType:
        return {
            "total_price": self.search_selector.get_total_price(),
            "cls_id": self.search_selector.cls_id(),
            "cls_name": self.search_selector.cls_name(),
            "where_to": models.F("route__node__town"),
            "where_from": models.F("route__origin__node__town"),
        }

    def get_queryset(self):
        route_join = self.search_selector.get_route_join()
        return self.query.select_related(*route_join).annotate(**self.get_annotate())

    def get_journies(self):
        data = self.get_queryset()
        self.search_selector.sync_route()
        for item in data:
            scales = self.search_selector.get_scales(item.route.origin.pk)
            setattr(item, "scales", scales)
            setattr(item, "has_scale", len(scales) >= 1)
            setattr(item, "passengers", self.search_selector.passengers())
            self.journies.append(item)
        return self.journies


def search_selector(manager: managers.JourneyManager, *args, **kwargs):
    cls_selector = ClsSelector()
    svc_route = Routes()
    price_selector = PriceSelector(query=cls_selector.query)
    route_selector = RouteSelector(route_services=svc_route)

    search = SearchSelector(
        cls_selector=cls_selector,
        route_selector=route_selector,
        price_selector=price_selector
    )

    jouries = JourneySelector(
        query=manager,
        search_selector=search,
    )

    print("data:===>", args, kwargs)
    search.request(*args, **kwargs)
    return jouries.get_journies()


def get_params_value(value: Union[INT_STR, list[int]]) -> INT_STR:
    return value[0] if isinstance(
        value, list
    ) and len(value) > 0 else value  # type: ignore
