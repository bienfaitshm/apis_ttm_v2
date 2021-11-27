from rest_framework import viewsets
from rest_framework import filters
from .filters.filters import IsComponyFilterBackend, SearchWhereFromToFilterBackend

from .serializers import (
    CarSerializer, CoverCitySerializer, JourneyMoreInfoSerializer, JourneySerializer, PointOfSaleSerializer,
    PointOfSaleWorkerSerializer, RoutingMoreInfoSerializer, RoutingSerializer, SeatSerializer,
    CabinePlaneSerializer, RouteJourneySerializer
)
from .models.technique import Cars, Seat, CabinePlane
from .models.transport import (
    CoverCity, Journey, PointOfSaleWorker, PointOfSale, Routing, RouteJourney
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


class JourneyView(viewsets.ModelViewSet):
    serializer_class = JourneySerializer
    queryset = Journey.objects.all()
    filter_backends = [filters.SearchFilter,
                       IsComponyFilterBackend, SearchWhereFromToFilterBackend]
    search_fields = ['numJourney', 'price']
    
    def get_serializer_class(self):
        if self.action == "list" or self.action =="retrieve":
            return JourneyMoreInfoSerializer
        return super().get_serializer_class()


class PointOfSaleWorkerView(viewsets.ModelViewSet):
    serializer_class = PointOfSaleWorkerSerializer
    queryset = PointOfSaleWorker.objects.all()
    filter_backends = [IsComponyFilterBackend,]


class PointOfSaleView(viewsets.ModelViewSet):
    serializer_class = PointOfSaleSerializer
    queryset = PointOfSale.objects.all()
    filter_backends = [IsComponyFilterBackend,]

class RouteJourneyView(viewsets.ModelViewSet):
    serializer_class =RouteJourneySerializer
    queryset =RouteJourney.objects.all()
    filter_backends = [IsComponyFilterBackend,]

class RoutingView(viewsets.ModelViewSet):
    serializer_class = RoutingSerializer
    queryset = Routing.objects.all()
    filter_backends = [IsComponyFilterBackend,]
    def get_serializer_class(self):
        if self.action == "list" or self.action =="retrieve":
            return RoutingMoreInfoSerializer
        return super().get_serializer_class()
