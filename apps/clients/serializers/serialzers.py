
from django.conf import settings
from rest_framework import serializers

from apps.clients import models as client_model
from apps.dash import models as dash_model
from utils import fields

default_device = ["USD", "CDF"]


class FretPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_model.FretPassenger
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_model.Passenger
        fields = "__all__"
        read_only_fields = ["journey"]


class JPassengersDataSerializer(serializers.Serializer):
    adult = serializers.IntegerField(default=settings.ADULT)
    child = serializers.IntegerField(default=settings.CHILD)
    inf = serializers.IntegerField(default=settings.INF)


class RSearchSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    where_from = serializers.CharField()
    where_to = serializers.CharField()
    datetime_from = serializers.DateTimeField()
    datetime_to = serializers.DateTimeField()
    duration = serializers.DateTimeField()
    passengers = JPassengersDataSerializer()
    j_class = serializers.CharField()
    j_class_id = serializers.IntegerField(default=0)
    total_price = serializers.FloatField()
    device = serializers.ChoiceField(choices=default_device, default="USD")
    has_scale = serializers.BooleanField(default=False)  # type: ignore
    scales = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    message = serializers.CharField(required=False)
    is_selected_for = serializers.BooleanField(default=False)  # type: ignore
    is_expired = serializers.BooleanField(default=False)  # type: ignore


class RSelectSerializer(JPassengersDataSerializer):
    session = serializers.CharField(read_only=True)
    journey = serializers.PrimaryKeyRelatedField(queryset=dash_model.Journey)
    j_class_id = serializers.PrimaryKeyRelatedField(
        queryset=dash_model.JourneyClass
    )


class RPassengerSerializer(serializers.Serializer):
    session = fields.SessionField(
        queryset=client_model.SeletectedJourney.objects.all(),
        required=True, write_only=True,
    )
    passengers = PassengerSerializer(many=True)


class R_OtherInfoSerializer(serializers.ModelSerializer):
    session = fields.SessionField(
        queryset=client_model.SeletectedJourney.objects.all(),
        required=True, write_only=True,
    )

    class Meta:
        model = client_model.OtherInfoReservation
        exclude = ["journey"]
        read_only_fields = []


class RCompletedSerializer(serializers.Serializer):
    booker = serializers.CharField(read_only=True)
    expire_datetime = serializers.DateTimeField(read_only=True)
    pnr = serializers.CharField(read_only=True)
    total_price = serializers.CharField(read_only=True)
    text_reservation = serializers.CharField(read_only=True)
    passengers = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        read_only=True
    )


class JourneyClientFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_model.JourneyClientFolder
        fields = "__all__"


class SeletectedJourneySerializer(serializers.ModelSerializer):
    session_key = serializers.CharField(source="session.key", read_only=True)

    class Meta:
        model = client_model.SeletectedJourney
        fields = "__all__"
        read_only_fields = ["folder", "session"]


class PlaceReservedSerializer(serializers.ModelSerializer):
    session = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = client_model.PlaceReserved
        fields = "__all__"
        read_only_fields = ["journey", "expired"]

    def create(self, validated_data):
        model = self.Meta.model
        print("#data", validated_data)
        return model.objects.none()


class JourneySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_model.JourneySession
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
