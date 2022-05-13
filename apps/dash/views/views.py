from rest_framework import viewsets
from rest_framework import filters
from ..filters.filters import FromWhereFromeFilterBackend, IsComponyFilterBackend
from ..filters.search_journey import SearchJourneyByDateFilters, SearchJourneyByDepartureFilters, SearchJourneyByDestinationFilters

from ..serializers import (
    CarSerializer, CoverCitySerializer, JourneyMoreInfoSerializer, JourneySerializer, PointOfSaleSerializer,
    PointOfSaleWorkerSerializer, RoutingMoreInfoSerializer, RoutingSerializer, SeatSerializer,
    CabinePlaneSerializer, JourneyTarifSerializer, JourneyClassSerializer
)
from ..models.technique import Cars, Seat, CabinePlane
from ..models.transport import (
    CoverCity, Journey, PointOfSaleWorker, PointOfSale, Routing, JourneyClass, JourneyTarif
)


class SeatView(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()


class CabinePlaneView(viewsets.ModelViewSet):
    serializer_class = CabinePlaneSerializer
    queryset = CabinePlane.objects.all()


class CarsView(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Cars.objects.all()


class SeatView(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()


class CoverCityView(viewsets.ModelViewSet):
    serializer_class = CoverCitySerializer
    queryset = CoverCity.objects.all()


class JourneyClassView(viewsets.ModelViewSet):
    serializer_class = JourneyClassSerializer
    queryset = JourneyClass.objects.all()


class JourneyTarifView(viewsets.ModelViewSet):
    serializer_class = JourneyTarifSerializer
    queryset = JourneyTarif.objects.all()


class JourneyView(viewsets.ModelViewSet):
    serializer_class = JourneySerializer
    queryset = Journey.objects.all()
    filter_backends = [filters.SearchFilter,
                       IsComponyFilterBackend, SearchJourneyByDateFilters,
                       SearchJourneyByDepartureFilters, SearchJourneyByDestinationFilters]
    search_fields = ['numJourney']

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return JourneyMoreInfoSerializer
        return super().get_serializer_class()


class PointOfSaleWorkerView(viewsets.ModelViewSet):
    serializer_class = PointOfSaleWorkerSerializer
    queryset = PointOfSaleWorker.objects.all()
    filter_backends = [IsComponyFilterBackend, ]


class PointOfSaleView(viewsets.ModelViewSet):
    serializer_class = PointOfSaleSerializer
    queryset = PointOfSale.objects.all()
    filter_backends = [IsComponyFilterBackend, ]


class RoutingView(viewsets.ModelViewSet):
    serializer_class = RoutingSerializer
    queryset = Routing.objects.all()
    filter_backends = [IsComponyFilterBackend, FromWhereFromeFilterBackend]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RoutingMoreInfoSerializer
        return super().get_serializer_class()
