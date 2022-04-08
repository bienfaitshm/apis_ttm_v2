from typing import Union

from apps.account.models import Users, Company
from utils.args_utils import kwargs_id_creator
from ..models import Routing, CoverCity


NodeType = Union[CoverCity, int]
LinkType = Union[Routing, None]


class RouteProcess:
    """
        "distance": 0.0,
        "company": 1,
        "node": 2,
        "whereFrom": null,
        "whereTo": null

    """
    @classmethod
    def create(cls, **kwargs):

        routing = Routing.objects.create(**kwargs_id_creator(**kwargs))

        return routing
