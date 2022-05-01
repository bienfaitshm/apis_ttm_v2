from abc import ABC, abstractmethod
from typing import Union

from requests import delete

from apps.account.models import Users, Company
from utils.args_utils import kwargs_id_creator
from ..models import Routing, CoverCity


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
    def insert_between(self, e: Routing, predecessor: Routing, successor: Routing) -> Routing:
        pass

    @abstractmethod
    def delete_node(self, e: Routing) -> Routing:
        pass

    @abstractmethod
    def first(self) -> Routing:
        pass


class RouteProcess(RouteProcessABC):
    """
        "distance": 0.0,
        "company": 1,
        "node": 2,
        "whereFrom": null,
        "whereTo": null

    """
    @classmethod
    def first(cls, destination: Routing) -> Union[CoverCity, None]:
        first = None
        current = destination
        while current != None:
            first = current.node
            current = current.whereFrom
        return first

    @classmethod
    def firstroute(cls, destination: Routing):
        first = None
        current = destination
        while current != None:
            first = current
            current = current.whereFrom
        return first

    @classmethod
    def last(cls, debut=Routing) -> Union[CoverCity, None]:
        last = None
        current = debut
        while current != None:
            last = current.node
            current = current.whereTo
        return last

    @classmethod
    def number_of_escale(cls, route: Routing):
        return len(cls.get_scale(route))

    @classmethod
    def get_scale(cls, route: Routing):
        escale = []
        current = cls.firstroute(route)
        while current != None:
            if hasattr(current, 'whereFrom') and hasattr(current, "whereTo") and current.whereFrom and current.whereTo:
                escale.append(current.node)
            current = current.whereTo
        return escale

    @classmethod
    def create(cls, **kwargs):
        routing: Routing = Routing.objects.create(
            **kwargs_id_creator(**kwargs))
        deb: Union[Routing, None] = routing.whereFrom
        # dest: Union[Routing,None]= routing.whereTo

        if deb != None:
            deb.whereTo = routing
            deb.save()
        return routing
