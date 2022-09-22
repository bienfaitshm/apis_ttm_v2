from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response

from apps.clients.selectors import selector_reservation
from apps.dash import models as dash_model

from ..models import (
    OtherInfoReservation, Passenger, ResearchReservation, SeletectedJourney,
)
from ..serializers import reservation as reserv_serializer
from ..serializers.reservation import (
    OtherInfoJourneyReservation, PassengerJourneyReservation,
    ReachercheJourneyReservationSerializer, SelectjourneyReservation,
)


class ReservationViewApis(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    reservations actions
    """
    serializer_class = reserv_serializer.JReservationSerializer
    # queryset = selector_reservation.find_reservation_journey()

    def get_queryset(self):
        return selector_reservation.find_reservation_journey()


class ReachercheJourneyReservationView(generics.CreateAPIView):
    queryset = ResearchReservation.objects.all()
    serializer_class = ReachercheJourneyReservationSerializer


class SelectJourneyreservationView(generics.CreateAPIView):
    queryset = SeletectedJourney.objects.all()
    serializer_class = SelectjourneyReservation


class PassengerJourneyReservationView(generics.CreateAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerJourneyReservation


class OtherInfoReservationView(generics.CreateAPIView):
    queryset = OtherInfoReservation.objects.all()
    serializer_class = OtherInfoJourneyReservation
