import datetime
from email.policy import default
from rest_framework import serializers
from django.utils.crypto import get_random_string
from utils import fields
from ..models import (
    FretPassenger, JourneyClientFolder, Passenger, SeletectedJourney, PlaceReserved,
    JourneySession, OtherInfoReservation, ValidationPayment
)

KEY = "1234567890qwertyuiopasdfghjklzxcvbnm<>,./?:;+_)(*&^%$#@!"


class FretPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FretPassenger
        fields = "__all__"


class OtherInfoReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherInfoReservation
        fields = "__all__"
        read_only_fields = ["journey"]
        extra_kwargs = {
        }


class ValidationPaymentSerializer(serializers.ModelSerializer):
    session = fields.SessionField(
        required=True, write_only=True,
        queryset=SeletectedJourney.objects.all()
    )

    class Meta:
        model = ValidationPayment
        fields = "__all__"
        read_only_fields = ["journey_selected"]


class JourneyClientFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyClientFolder
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"
        read_only_fields = ["journey"]


class SeletectedJourneySerializer(serializers.ModelSerializer):
    session_key = serializers.CharField(source="session.key", read_only=True)

    class Meta:
        model = SeletectedJourney
        fields = "__all__"
        read_only_fields = ["folder", "session"]


class PlaceReservedSerializer(serializers.ModelSerializer):
    session = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = PlaceReserved
        fields = "__all__"
        read_only_fields = ["journey", "expired"]

    def create(self, validated_data):
        model = self.Meta.model
        print("#data", validated_data)
        return model.objects.none()


class JourneySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneySession
        fields = "__all__"


class SelectJourneyStepOneSerializer(serializers.Serializer):
    journey = serializers.IntegerField()


def positive_interger(value):
    if value < 0:
        raise serializers.ValidationError('Not a multiple of ten')


class JourneyClientFolderMoreSerializer(JourneyClientFolderSerializer):
    reservations = SeletectedJourneySerializer(many=True, default=[])

    class Meta(JourneyClientFolderSerializer.Meta):
        pass


class SeletectedJourneyMoreSerializer(SeletectedJourneySerializer):
    passengers = PassengerSerializer(many=True, default=[])

    class Meta(SeletectedJourneySerializer.Meta):
        pass
