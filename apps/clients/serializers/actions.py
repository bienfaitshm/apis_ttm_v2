from rest_framework import serializers
from ..models import (Passenger, JourneyClientFolder, Client,
                      OtherInfoReservation, JourneySession, SeletectedJourney)

# from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.contrib.sessions.middleware import SessionMiddleware


class SplitFolderSerialiser(serializers.Serializer):
    folder = serializers.PrimaryKeyRelatedField(
        queryset=JourneyClientFolder.objects.all())
    passengers = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), write_only=True)
