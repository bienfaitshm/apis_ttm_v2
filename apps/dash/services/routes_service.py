from abc import ABC, abstractmethod
from typing import Any, Union

from django.db.models import BaseManager

from apps.dash.models import CoverCity, Routing
from utils.args_utils import kwargs_id_creator

NodeType = Union[CoverCity, int]
LinkType = Union[Routing, None]


class RouteProcessABC(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def insert_between(
        self,
        e: Routing,
        predecessor: Routing,
        successor: Routing
    ) -> Routing:
        pass

    @abstractmethod
    def delete_node(self, e: Routing) -> Routing:
        pass

    @abstractmethod
    def first(self) -> Routing:
        pass

    @abstractmethod
    def create(self, *args, **kwargs) -> Routing:
        pass


class RouteProcess(RouteProcessABC):
    """
        "distance": 0.0,
        "company": 1,
        "node": 2,
        "whereFrom": null,
        "whereTo": null

    """

    def get_obj(self):
        return Routing.objects

    @classmethod
    def first(cls, destination: Routing) -> Union[CoverCity, None]:
        if first_route := cls.firstroute(destination=destination):
            return first_route.node

    @classmethod
    def firstroute(cls, destination: Routing) -> LinkType:
        first = None
        current = destination
        while current != None:
            first = current
            current = current.whereFrom
        return first

    @classmethod
    def last(cls, debut=Routing) -> Union[CoverCity, None]:
        if last_route := cls.last_route(route=debut):
            return last_route.node

    @classmethod
    def last_route(cls, route=Routing) -> LinkType:
        last = None
        current = route
        while current != None:
            last = current
            current = current.whereTo
        return last

    @classmethod
    def is_last_route(cls, route=Routing) -> bool:
        last_route = cls.last_route(route)
        return last_route.pk == route.pk

    @classmethod
    def number_of_escale(cls, route: Routing):
        return cls.get_scale(route=route).count()

    @classmethod
    def get_scale(cls, route: Routing):
        return cls.get_obj(cls).filter(origin=route.origin)  # .order_by("")

    @classmethod
    def create(cls, **kwargs):
        _where_from_value = kwargs.get("whereFrom")

        # get the whereFrom in params
        where_from: LinkType = Routing.objects.filter(
            pk=_where_from_value
        ).select_related("origin", "whereFrom").first()

        params = kwargs_id_creator(**kwargs)
        if where_from is not None:
            params["origin"] = where_from if (
                where_from.whereFrom is None
            ) else where_from.origin

        routing: Routing = Routing.objects.create(**params)

        if where_from is not None:
            where_from.whereTo = routing
            where_from.save()
        return routing


def create_route() -> Union[Routing, None]:
    return
