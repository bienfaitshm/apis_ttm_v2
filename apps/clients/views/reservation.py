from rest_framework import generics

from ..serializers.reservation import PassengerJourneyReservation, SelectjourneyReservation, OtherInfoJourneyReservation
from ..models import SeletectedJourney, Passenger, OtherInfoReservation


class SelectJourneyreservationView(generics.CreateAPIView):
    queryset = SeletectedJourney.objects.all()
    serializer_class = SelectjourneyReservation


class PassengerJourneyReservationView(generics.CreateAPIView):
    queryset = Passenger.objects.all()
    serializer_class = PassengerJourneyReservation


class OtherInfoReservationView(generics.CreateAPIView):
    queryset = OtherInfoReservation.objects.all()
    serializer_class = OtherInfoJourneyReservation
