from rest_framework import serializers
from .models import (
    FretPassenger, JourneyClientFolder, Passenger, SeletectedJourney, PlaceReserved,
    JourneySession
)


class FretPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FretPassenger
        fields = "__all__"


class JourneyClientFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyClientFolder
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class SeletectedJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeletectedJourney
        fields = "__all__"


class PlaceReservedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceReserved
        fields = "__all__"


class JourneySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneySession
        fields = "__all__"


class SelectJourneyStepOneSerializer(serializers.Serializer):
    selected = SeletectedJourneySerializer()


class SetNumberOfPassengerStepTwoSerializer(serializers.Serializer):
    pass


class InputPassengerInfoStepThreeSerializer(serializers.Serializer):
    pass


class SelectSeatOfPassengerStepForSerializer(serializers.Serializer):
    pass


class SetFretStepFiveSerializer(serializers.Serializer):
    pass


class PayementStepSixSerializer(serializers.Serializer):
    pass


class ValideStepFinalSerializer(serializers.Serializer):
    pass
