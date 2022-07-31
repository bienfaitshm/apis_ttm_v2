from rest_framework import generics

from ..models import (
    OtherInfoReservation, Passenger, ResearchReservation, SeletectedJourney,
)
from ..serializers.reservation import (
    OtherInfoJourneyReservation, PassengerJourneyReservation,
    ReachercheJourneyReservationSerializer, SelectjourneyReservation,
)


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
