import contextlib

from collections import OrderedDict, deque
from dataclasses import dataclass, field
from typing import List, Literal, Optional, Tuple, TypedDict, Union

from django.db import models

from apps.dash.models import Routing

ROUTE_NONE = Union[None, Routing]
ROUTE_DICT_DATA = OrderedDict[Union[str, int], List[Routing]]
ROUTE_DATA = OrderedDict[str, Routing]


class RouteDictType(TypedDict):
    id: int
    origin: int
    town: int
    code: int
    whereFrom: int
    whereTo: int
    level: int


def initial_value():
    return OrderedDict()


@dataclass
class Routes:
    ordered_data: ROUTE_DICT_DATA = field(
        init=False, default_factory=initial_value)
    queryset = Routing.objects
    inner_joins = (
        "node", "origin",
        "origin__node", "whereFrom",
        "whereTo", "whereFrom__node",
        "whereFrom__node"
    )

    @property
    def get_routes(self):
        return self.queryset.all().select_related(*self.inner_joins)

    def create(
        self,
        where_from: Union[Routing, int, str],
        *args, **kwargs
    ) -> Union[Tuple[Literal[False], str], Tuple[Literal[True], Routing]]:
        """ create new route"""

        if isinstance(where_from, (int, str)):
            with contextlib.suppress(Routing.DoesNotExist):
                where_from = Routing.objects.get(pk=where_from)

        next_level = 0
        origin = None
        if isinstance(where_from, Routing):
            next_level = where_from.level + 1
            origin = where_from.origin or where_from

        next_route = Routing.objects.create(
            origin=origin,
            whereFrom=where_from,
            level=next_level,
            **kwargs
        )

        if isinstance(where_from, Routing):
            where_from.whereTo = next_route  # type: ignore
            where_from.origin = origin  # type: ignore
            where_from.save()
        return True, next_route

    def get_origin(self, route: ROUTE_NONE) -> ROUTE_NONE:
        if route and isinstance(route, Routing):
            return route.origin

        with contextlib.suppress(Routing.DoesNotExist):
            _route = Routing.objects.get(pk=route)
            return _route.origin

    def get_end_routes(self, route: ROUTE_NONE) -> ROUTE_NONE:
        if isinstance(route, Routing):
            with contextlib.suppress(Routing.DoesNotExist):
                return Routing.objects.get(
                    origin=route.origin,
                    whereTo=None
                )

    def get_scales(self, route: ROUTE_NONE):
        if isinstance(route, Routing):
            return Routing.objects.exclude(
                models.Q(whereFrom=None) | models.Q(whereTo=None)
            ).filter(origin=route.origin)\
                .select_related()

        return Routing.objects.none()

    def sync(self):
        data = self.get_routes
        for i in data:
            if i.origin is None:
                continue
            if i.origin.pk in self.ordered_data:
                self.ordered_data[i.origin.pk].append(i)
            else:
                self.ordered_data[i.origin.pk] = [i]

    @property
    def _data(self) -> ROUTE_DICT_DATA:
        return self.ordered_data

    def get_scales_in_ordered(
        self,
        origin: Union[str, int],
        routes: Optional[List[Routing]] = None
    ):
        scales = deque([])
        data: List[Routing] = routes or self.ordered_data.get(str(origin), [])
        for item in data:
            if item.whereFrom is not None and item.whereTo is not None:
                scales.append(item)
        return scales

    def get_scales_from_all(self, orgin):
        pass

    def get_routes_data(self):
        self.sync()
        _tmp = deque([])
        d = self._data
        for origin, route_chain in d.items():
            scales = self.get_scales_in_ordered(origin)
            _dict = OrderedDict()

            for item in route_chain:
                if item.whereFrom is None:
                    _dict["where_from"] = item
                if item.whereTo is None:
                    _dict["where_to"] = item

            _dict["scales"] = scales
            _dict["has_scale"] = len(scales) >= 1
            _tmp.append(_dict)
        return _tmp
