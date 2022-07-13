
from rest_framework import viewsets, filters
from django.utils.translation import gettext as _
from apps.dash.filters.filters import IsComponyFilterBackend
from utils import methods

from ..models import (
    FretPassenger, JourneyClientFolder, PlaceReserved, SeletectedJourney,
    JourneySession, Passenger,
)
from ..serializers import serialzers as sz


class FretPassengerView(viewsets.ModelViewSet):
    serializer_class = sz.FretPassengerSerializer
    queryset = FretPassenger.objects.all()


class JourneyClientFolderView(viewsets.ModelViewSet):
    serializer_class = sz.JourneyClientFolderSerializer
    queryset = JourneyClientFolder.objects.all()
    filter_backends = [filters.SearchFilter, IsComponyFilterBackend]
    search_fields = ['number']

    def get_serializer_class(self):
        if self.action is methods.RETRIEVE:
            return sz.JourneyClientFolderMoreSerializer
        return super().get_serializer_class()


class PlaceReservedView(viewsets.ModelViewSet):
    serializer_class = sz.PlaceReservedSerializer
    queryset = PlaceReserved.objects.all()


class SeletectedJourneyView(viewsets.ModelViewSet):
    serializer_class = sz.SeletectedJourneySerializer
    queryset = SeletectedJourney.objects.all()

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
