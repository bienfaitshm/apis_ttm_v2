import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from .types import (
    CarsType, SeatType, CabinePlaneType, CompanyType,
    EmployeType,CoverCityType,JourneyType,
    PointOfSaleType,PointOfSaleWorkerType, RoutingType
)



from .models import (
    CabinePlane,PointOfSale,Cars,Company,
    CoverCity,Employe,Journey,
    PointOfSaleWorker,Routing,Seat
)

class Query(graphene.ObjectType):
    car = relay.Node.Field(CarsType)
    cars = DjangoFilterConnectionField(CarsType)

    seat = relay.Node.Field(SeatType)
    seats = DjangoFilterConnectionField(SeatType)

    cabine_plane = relay.Node.Field(CabinePlaneType)
    cabine_planes = DjangoFilterConnectionField(CabinePlaneType)

    company = relay.Node.Field(CompanyType)
    companies = DjangoFilterConnectionField(CompanyType)

    cover_city = relay.Node.Field(CoverCityType)
    cover_cities = DjangoFilterConnectionField(CoverCityType)

    journey = relay.Node.Field(JourneyType)
    journies = DjangoFilterConnectionField(JourneyType)

    pos = relay.Node.Field(PointOfSaleType)
    poss = DjangoFilterConnectionField(PointOfSaleType)

    pos_worker = relay.Node.Field(PointOfSaleWorkerType)
    pos_workers = DjangoFilterConnectionField(PointOfSaleWorkerType)

    employe = relay.Node.Field(EmployeType)
    employes = DjangoFilterConnectionField(EmployeType)

    routing = relay.Node.Field(RoutingType)
    routings = DjangoFilterConnectionField(RoutingType)


class Mutation(graphene.ObjectType):
    pass
    