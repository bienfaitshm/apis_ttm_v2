
from rest_framework import viewsets

from utils import methods

from ..models import (
    FretPassenger, JourneySession, Passenger, PlaceReserved, SeletectedJourney,
)
from ..serializers import serialzers as sz


class FretPassengerView(viewsets.ModelViewSet):
    serializer_class = sz.FretPassengerSerializer
    queryset = FretPassenger.objects.all()


class PlaceReservedView(viewsets.ModelViewSet):
    serializer_class = sz.PlaceReservedSerializer
    queryset = PlaceReserved.objects.all()


class SeletectedJourneyView(viewsets.ModelViewSet):
    serializer_class = sz.SeletectedJourneySerializer
    queryset = SeletectedJourney.objects.all()\
        .select_related("session", "journey", "journey_class")
    # .prefetch_related("passengers")

    def get_serializer_class(self):
        if self.action is methods.RETRIEVE:
            return sz.SeletectedJourneyMoreSerializer
        return super().get_serializer_class()


class JourneySessionView(viewsets.ModelViewSet):
    serializer_class = sz.JourneySessionSerializer
    queryset = JourneySession.objects.all()


class PassengerView(viewsets.ModelViewSet):
    serializer_class = sz.PassengerSerializer
    queryset = Passenger.objects.all()
