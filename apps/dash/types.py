# import graphene
from graphene_django import DjangoObjectType
from utils.user_mixin import UserMixin
from utils.node import CustomNode

from .models import (
    CabinePlane,PointOfSale,Cars,Company,
    CoverCity,Employe,Journey,
    PointOfSaleWorker,Routing,Seat
)

class MixinType(UserMixin, DjangoObjectType):
    class Meta:
        interfaces = (CustomNode,)
        filter_fields = []
        fields = "__all__"

class CabinePlaneType(MixinType):
    class Meta(MixinType.Meta):
        model = CabinePlane

class PointOfSaleType(MixinType):
    class Meta(MixinType.Meta):
        model = PointOfSale

class CarsType(MixinType):
    class Meta(MixinType.Meta):
        model = Cars

class CompanyType(MixinType):
    class Meta(MixinType.Meta):
        model = Company


class CoverCityType(MixinType):
    class Meta(MixinType.Meta):
        model = CoverCity

class EmployeType(MixinType):
    class Meta(MixinType.Meta):
        model = Employe

class JourneyType(MixinType):
    class Meta(MixinType.Meta):
        model = Journey

class PointOfSaleWorkerType(MixinType):
    class Meta(MixinType.Meta):
        model = PointOfSaleWorker

class RoutingType(MixinType):
    class Meta(MixinType.Meta):
        model = Routing

class SeatType(MixinType):
    class Meta(MixinType.Meta):
        model = Seat