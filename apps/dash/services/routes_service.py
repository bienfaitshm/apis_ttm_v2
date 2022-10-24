from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from typing import Union

from django.db import connection

from apps.dash.models import CoverCity, Routing
from utils.args_utils import kwargs_id_creator

from .route_sql import recursive_route_sql

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


@dataclass
class RouteCreatorService:
    def create(self, *args, **kwargs):
        pass


class RouteServices:
    init_route: Union[str, int]
    routes = {}
    deeper = 0

    def __init__(self, route) -> None:
        self.routes = {}
        self.fix_data(route)

    def fix_data(self, route):
        obj = queryset_routes(route)
        for item in obj:
            if item.level in self.routes:
                if item.level >= 1:
                    previous_item = self.routes[item.level-1]
                    if item.id == previous_item.whereTo:
                        self.routes[item.level] = item
                if item.whereTo is None:
                    break
            else:
                self.routes[item.level] = item
                self.deeper = item.level

    def get_routes(self):
        return [value for _, value in self.routes.items()]

    def get_deeper(self):
        return self.deeper

    def get_where_from(self):
        return self.routes.get(0)

    def get_where_to(self):
        return self.routes.get(self.deeper)

    def get_scales(self):
        excludes = [0, self.deeper]
        return [
            value for key, value in self.routes.items() if key not in excludes
        ]


def namedtuplefetchall(route):
    "Return all rows from a cursor as a namedtuple"
    desc = route.description
    nt_result = namedtuple('Route', [col[0] for col in desc])
    return [nt_result(*row) for row in route.fetchall()]


def queryset_routes(route=9):
    with connection.cursor() as cursor:
        cursor.execute(recursive_route_sql, [route])
        row = namedtuplefetchall(cursor)
    return row


def recursive():
    service = RouteServices(route=7)
    re = service.get_scales()
    print("recursive", re)
    # for item in re:
    #     print("===>", item)


def create_route() -> Union[Routing, None]:
    return
