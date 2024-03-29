from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets

from apps.dash.filters.routes import FilterRouteType
from utils import methods

from ..filters.filters import IsComponyFilterBackend
from ..filters.search_journey import (
    FilterIntensive, SearchJourneyByDateFilters,
    SearchJourneyByDepartureFilters, SearchJourneyByDestinationFilters,
)
from ..models.technique import CabinePlane, Cars, Seat
from ..models.transport import (
    CoverCity, Journey, JourneyClass, JourneyTarif, PointOfSale,
    PointOfSaleWorker, Routing,
)
from ..serializers import (
    CabinePlaneSerializer, CarSerializer, CoverCitySerializer,
    JourneyClassSerializer, JourneyMoreInfoSerializer, JourneySerializer,
    JourneyTarifSerializer, PointOfSaleSerializer, PointOfSaleWorkerSerializer,
    RoutingMoreInfoSerializer, RoutingSerializer, SeatSerializer,
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
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        IsComponyFilterBackend,
        SearchJourneyByDateFilters,
        SearchJourneyByDepartureFilters,
        SearchJourneyByDestinationFilters,
        FilterIntensive
    ]
    search_fields = ['numJourney']
    filterset_fields = [
        'dateDeparture',
        'dateReturn',
        'route',
        'numJourney',
    ]

    def get_serializer_class(self):
        if self.action in methods.DETAIL_METHODS:
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
    filter_backends = [FilterRouteType, IsComponyFilterBackend]

    def get_serializer_class(self):
        # get the specifique serializers on method of reading
        if self.action in methods.DETAIL_METHODS:
            return RoutingMoreInfoSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return self.queryset.select_related("whereTo", "node")
