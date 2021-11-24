import graphene
from graphene_django import DjangoObjectType
import datetime
from utils import node
from utils.user_mixin import UserMixin

from .models import (
    CabinePlane,PointOfSale,Cars,Company,
    CoverCity,Employe,Journey,
    PointOfSaleWorker,Routing,Seat
)

# class MixinType(UserMixin, DjangoObjectType):
#     class Meta:
#         interfaces = (node.CustomNode,)
#         filter_fields = []
#         fields = "__all__"

class CabinePlaneType(UserMixin, DjangoObjectType):
    number_of_seats = graphene.Int()
    class Meta:
        model = CabinePlane
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"
    def resolve_number_of_seats(self, info):
        return self.number_of_seats

class PointOfSaleType(UserMixin, DjangoObjectType):
    class Meta:
        model = PointOfSale
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class CarsType(UserMixin, DjangoObjectType):
    class Meta:
        model = Cars
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class CompanyType(UserMixin, DjangoObjectType):
    class Meta:
        model = Company
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"


class CoverCityType(UserMixin, DjangoObjectType):
    class Meta:
        model = CoverCity
        interfaces = (node.CustomNode,)
        filter_fields = {
            'town':['exact', 'icontains', 'istartswith'],
            'code':['exact', 'icontains', 'istartswith'],
        }
        fields = "__all__"

class EmployeType(UserMixin, DjangoObjectType):
    class Meta:
        model = Employe
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class JourneyType(UserMixin, DjangoObjectType):
    number_of_places_reserved = graphene.Int()
    is_direct = graphene.Boolean()
    exprired = graphene.Boolean()
    route_names = graphene.String()
    class Meta:
        model = Journey
        interfaces = (node.CustomNode,)
        filter_fields = {
            'company__nom': ['exact', 'icontains', 'istartswith'],
            'company__code': ['exact'],
            'company__id': ['exact'],
            'routes__whereFrom__town':['exact', 'icontains', 'istartswith'],
            'routes__whreTo__town':['exact', 'icontains', 'istartswith'],
        }
        fields = "__all__"
    
    def resolve_number_of_places_reserved(self, info):
        return self.number_places_taken()

class PointOfSaleWorkerType(UserMixin, DjangoObjectType):
    class Meta:
        model = PointOfSaleWorker
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class RoutingType(UserMixin, DjangoObjectType):
    class Meta:
        model = Routing
        interfaces = (node.CustomNode,)
        filter_fields = {
            'whereFrom__town':['exact', 'icontains', 'istartswith'],
            'whreTo__town':['exact', 'icontains', 'istartswith'],
        }
        fields = "__all__"

class SeatType(UserMixin, DjangoObjectType):
    class Meta:
        model = Seat
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"