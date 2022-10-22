
from django.conf import settings
from rest_framework import exceptions, serializers

from apps.clients import models as client_model
from apps.clients.serializers.validators import journey_expired_validator
from apps.clients.services import reservations_services as r_services
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
    id = serializers.IntegerField()
    where_from = serializers.CharField(default="")
    where_to = serializers.CharField(default="")
    datetime_from = serializers.DateTimeField()
    datetime_to = serializers.DateTimeField()
    duration = serializers.CharField()
    passengers = JPassengersDataSerializer(default=[])
    cls_name = serializers.CharField(default="")
    cls_id = serializers.IntegerField(default=1)
    total_price = serializers.FloatField(default=0)
    device = serializers.ChoiceField(choices=default_device, default="USD")
    has_scale = serializers.BooleanField(default=False)  # type: ignore
    scales = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=[],
    )
    message = serializers.CharField(required=False)
    is_selected_for = serializers.BooleanField(default=False)  # type: ignore
    is_expired = serializers.BooleanField(default=False)  # type: ignore


class RSelectSerializer(JPassengersDataSerializer):
    session = serializers.CharField(read_only=True)
    journey = serializers.PrimaryKeyRelatedField(
        queryset=dash_model.Journey.objects.all(),
        validators=[journey_expired_validator],
        write_only=True
    )
    j_class_id = serializers.PrimaryKeyRelatedField(
        queryset=dash_model.JourneyClass.objects.all(),
        write_only=True
    )

    def create(self, validated_data: dict):
        j_cls = validated_data.pop("j_class_id")
        baby = validated_data.pop("inf")
        r_service = r_services.ReservationServices(session=None)
        succes, value = r_service.create_reservation(
            j_cls=j_cls, baby=baby, **validated_data)

        if not succes:
            raise exceptions.ValidationError(value)
        return {
            "session": value.session.key  # type: ignore
        }


class RPassengerSerializer(serializers.Serializer):
    session = fields.SessionField(
        queryset=client_model.SeletectedJourney.objects.all(),
        required=True, write_only=True,
    )
    passengers = PassengerSerializer(many=True)

    def create(self, validated_data):
        session = validated_data.get("session")
        psg = validated_data.get("passengers")
        r_service = r_services.ReservationServices(session=session)
        success, value = r_service.passengers(psg=psg)
        if not success:
            raise exceptions.ValidationError(value)
        return {
            "session": session.session.key,
            "passengers": value
        }


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
