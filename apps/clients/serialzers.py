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
    journey = serializers.IntegerField()


def positive_interger(value):
    if value < 0:
        raise serializers.ValidationError('Not a multiple of ten')


class SetNumberOfPassengerStepTwoSerializer(serializers.Serializer):
    numberAdult = serializers.IntegerField(validators=[positive_interger])
    numberChild = serializers.IntegerField(validators=[positive_interger])
    numberBaby = serializers.IntegerField(validators=[positive_interger])

    # def validate(self, data):
    #     """
    #         Check if one user must exist
    #     """
    #     if (data["numberAdult"] == 0 and data["numberBaby"] >= 1):
    #         raise serializers.ValidationError("baby can't go alone!")
    #     return data

    def update(self, instance, validated_data):
        instance.numberAdult = validated_data.get(
            'numberAdult', instance.numberAdult)
        instance.numberChild = validated_data.get(
            'numberChild', instance.numberChild)
        instance.numberBaby = validated_data.get(
            'numberBaby', instance.numberBaby)
        instance.last_step = 2
        instance.save()
        return instance


class InputPassengerInfoStepThreeSerializer(serializers.Serializer):
    passengers = PassengerSerializer(many=True)

    def create(self, validated_data):
        items = [Passenger(**item) for item in validated_data]
        return Passenger.objects.bulk_create(items)


class SelectSeatOfPassengerStepForSerializer(serializers.Serializer):
    pass


class SetFretStepFiveSerializer(serializers.Serializer):
    pass


class PayementStepSixSerializer(serializers.Serializer):
    pass


class ValideStepFinalSerializer(serializers.Serializer):
    pass
