import contextlib

from dataclasses import dataclass
from typing import Literal, Tuple, Union

from django.db import models

from apps.dash.models import Routing

ROUTE_NONE = Union[None, Routing]


@dataclass
class Routes:

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
                .select_related("node", "origin", "origin__node")

        return Routing.objects.none()
