from unittest import result
from rest_framework import serializers
from apps.clients.serializers.serialzers import OtherInfoReservationSerializer, PassengerSerializer
from apps.dash.models import JourneyClass
from utils import fields
from ..models import OtherInfoReservation, SeletectedJourney, Passenger
from ..process.reservation import ReservationJourney


class SelectjourneyReservation(serializers.ModelSerializer):
    info = serializers.SerializerMethodField(
        method_name="get_info", read_only=True)
    session_key = serializers.CharField(source="session.key", read_only=True)
    journey_class = serializers.PrimaryKeyRelatedField(
        queryset=JourneyClass.objects.all(), write_only=True)

    class Meta:
        model = SeletectedJourney
        fields = "__all__"
        read_only_fields = ['session', 'folder', 'session_key']
        extra_kwargs = {
            'journey_class': {'write_only': True}
        }

    def create(self, validated_data: dict):
        self.tmp = validated_data.pop("journey_class")
        return ReservationJourney.select_journey(**validated_data)

    def get_info(self, objet):
        return str(self.tmp)


class PassengerJourneyReservation(serializers.Serializer):
    session = fields.SessionField(
        required=True, write_only=True,
        queryset=SeletectedJourney.objects.all()
    )
    passengers = PassengerSerializer(many=True, write_only=True)

    def create(self, validated_data: dict):
        passengers: list = validated_data.get("passengers")
        session = validated_data.get("session")
        result = Passenger.objects.bulk_create([
            Passenger(**i, journey=session) for i in passengers
        ])
        print(validated_data)
        return result


class OtherInfoJourneyReservation(serializers.Serializer):
    session = fields.SessionField(
        required=True, write_only=True,
        queryset=SeletectedJourney.objects.all()
    )
    other_info = OtherInfoReservationSerializer(write_only=True)

    def create(self, validated_data: dict):
        other_info: list = validated_data.get("other_info")
        session = validated_data.get("session")
        result = OtherInfoReservation.objects.create(
            **other_info, journey=session)
        return result
