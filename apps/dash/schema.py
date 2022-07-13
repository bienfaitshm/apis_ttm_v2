import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .types import (
    CarsType, SeatType, CabinePlaneType, CompanyType,
    EmployeType, CoverCityType, JourneyType,
    PointOfSaleType, PointOfSaleWorkerType, RoutingType
)


from .models import (
    CabinePlane, PointOfSale, Cars, Company,
    CoverCity, Employe, Journey,
    PointOfSaleWorker, Routing, Seat
)

from utils.node import CustomNode


class Query(graphene.ObjectType):
    car = CustomNode.Field(CarsType)
    cars = DjangoFilterConnectionField(CarsType)

    seat = CustomNode.Field(SeatType)
    seats = DjangoFilterConnectionField(SeatType)

    cabine_plane = CustomNode.Field(CabinePlaneType)
    cabine_planes = DjangoFilterConnectionField(CabinePlaneType)

    company = CustomNode.Field(CompanyType)
    companies = DjangoFilterConnectionField(CompanyType)

    cover_city = CustomNode.Field(CoverCityType)
    cover_cities = DjangoFilterConnectionField(CoverCityType)

    journey = CustomNode.Field(JourneyType)
    journies = DjangoFilterConnectionField(JourneyType)

    pos = CustomNode.Field(PointOfSaleType)
    poss = DjangoFilterConnectionField(PointOfSaleType)

    pos_worker = CustomNode.Field(PointOfSaleWorkerType)
    pos_workers = DjangoFilterConnectionField(PointOfSaleWorkerType)

    employe = CustomNode.Field(EmployeType)
    employes = DjangoFilterConnectionField(EmployeType)

    routing = CustomNode.Field(RoutingType)
    routings = DjangoFilterConnectionField(RoutingType)


class Mutation(graphene.ObjectType):
    pass
