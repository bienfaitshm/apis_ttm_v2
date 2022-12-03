import typing

from collections import OrderedDict, deque
from dataclasses import dataclass, field

from django.db import models
from django.db.models import OuterRef, Subquery

INT_STR = typing.Union[str, int]
QUERYSET = models.QuerySet[typing.Any]
FIELD_PASENGER_TYPE = typing.Union[
    typing.Literal["adult"],
    typing.Literal["child"],
    typing.Literal["baby"]
]


class RouteServiceProtocol(typing.Protocol):
    def sync(self) -> None:
        ...

    def get_scales_in_ordered(
        self,
        origin: INT_STR
    ) -> typing.Union[deque, list]:
        ...


class PriceSelectorProtocol(typing.Protocol):
    def get_total_price(self, *args, **kwargs): ...
    def get_unit_price(self, field): ...
    def get_adult_unit_price(self): ...
    def get_child_unit_price(self): ...
    def get_inf_unit_price(self): ...
    def get_taxe_price(self): ...
    def get_device(self): ...


@dataclass
class ClsSelector:
    queryset: models.QuerySet[typing.Any]
    out_ref: OuterRef = field(
        init=False,
        default_factory=lambda: OuterRef("route")
    )

    # field
    cls_field = "journey_class"
    cls_field_name = f"{cls_field}__name"
    cls_join = (cls_field_name,)

    def get_filter(self) -> typing.Dict[str, typing.Any]:
        return {
            "route": self.out_ref
        }

    @property
    def query(self):
        return self.queryset.filter(
            route=self.out_ref
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
    route_services: RouteServiceProtocol
    route_join = (
        "route",
        "route__node",
        "route__origin",
        "route__origin__node",
    )

    def get_route_join(self):
        return self.route_join

    def sync_route(self) -> None:
        self.route_services.sync()

    def get_scales(self, origin: INT_STR) -> typing.List[str]:
        scales = self.route_services.get_scales_in_ordered(origin)
        return [i.node.town for i in scales]


@dataclass
class PriceSelector(PriceSelectorProtocol):
    """
    Info of price of route
    Returns:
        taxe(adult, child, inf)
        adult_unit_price
        child_unit_price
        inf_unit_price
        total_price
        devise

    """
    queryset: models.QuerySet[typing.Any]
    adult: int = 1
    child: int = 0
    inf: int = 0

    def ptt(self, name: str = "adult"):
        """ prix toutes taxe confondu """
        return models.F(name) * ((models.F("taxe") / 100) + 1)

    def get_field(
        self,
        queryset,
        output_field: models.Field = models.FloatField()
    ):
        return Subquery(
            queryset=queryset,  # type: ignore
            output_field=output_field
        )

    def get_unit_price(self, field: FIELD_PASENGER_TYPE = "adult"):
        return self.get_field(queryset=self.queryset.values(field))

    def get_adult_unit_price(self):
        return self.get_unit_price()

    def get_child_unit_price(self):
        return self.get_unit_price(field="child")

    def get_inf_unit_price(self):
        return self.get_unit_price(field="baby")

    def get_taxe_price(self):
        return self.get_field(queryset=self.queryset.values("taxe"))

    def get_device(self):
        return self.get_field(
            queryset=self.queryset.values("devise"),
            output_field=models.CharField()
        )

    def f_total_price(
        self,
        adult: typing.Any = None,
        child: typing.Any = None,
        inf: typing.Any = None
    ):
        _adult = adult or self.adult
        _child = child or self.child
        _inf = inf or self.inf
        return (models.F("tp_ad") * _adult) + (models.F("tp_chd") * _child) + (models.F("tp_inf") * _inf)

    def get_total_price(self, *args, **kwargs):
        return Subquery(
            queryset=self.queryset.annotate(
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

    def set_passengers(self, adult: int, child: int, inf: int):
        self.adult = adult
        self.child = child
        self.inf = inf

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
