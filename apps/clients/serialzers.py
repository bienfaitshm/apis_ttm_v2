import datetime
from rest_framework import serializers
from django.utils.crypto import get_random_string
from utils  import fields
from .models import (
    FretPassenger, JourneyClientFolder, Passenger, SeletectedJourney, PlaceReserved,
    JourneySession
)

KEY = "1234567890qwertyuiopasdfghjklzxcvbnm<>,./?:;+_)(*&^%$#@!"

class FretPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FretPassenger
        fields = "__all__"


class JourneyClientFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyClientFolder
        fields = "__all__"


class PassengerSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="typeUser", read_only=True)
    sexe = serializers.CharField(source="gender", read_only=True)
    class Meta:
        model = Passenger
        fields = "__all__"
        read_only_fields = ["journey"]
        


class SeletectedJourneySerializer(serializers.ModelSerializer):
    session_key = serializers.CharField(source="session.key", read_only=True)
    class Meta:
        model = SeletectedJourney
        fields = "__all__"
        read_only_fields =["folder","session"]
    
    def create(self, validated_data):
        key =  get_random_string(10,KEY)
        date_expiration = datetime.datetime.now().date() + datetime.timedelta(days=2)
        request = self.context.get("request")
        cookie = request.headers.get("Cookie")
        folder = self.get_JourneyClientFolder(cookie)
        session = JourneySession.objects.create(key=key, dateExpiration = date_expiration)
        valide_data = {**validated_data, "folder":folder, "session":session}
        return super().create(valide_data)

    def get_JourneyClientFolder(self, session):
        num = get_random_string(5,"1234567890AB")
        try:
            return JourneyClientFolder.objects.get(session = session)
        except JourneyClientFolder.DoesNotExist:
            return JourneyClientFolder.objects.create(session = session, number= num)


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
    journey_selected = SeletectedJourneySerializer(read_only=True)
    passengers = PassengerSerializer(many=True, write_only=True)
    session = fields.SessionField(
        required = True, write_only=True,
        queryset = SeletectedJourney.objects.all()
    )
    class Meta:
        model = SeletectedJourney
        read_only_fields = ["journey_selected"]
        write_only_fields = ["passengers","session"]

    def create(self, validated_data):
        response = {}
        selected_journey = validated_data.get("session")
        passengers = validated_data.get("passengers")
        selected_journey.last_step = 2
        selected_journey.save()
        items = [
            Passenger(journey=selected_journey, **item) for item in passengers
        ]
        Passenger.objects.bulk_create(items)
        response["journey_selected"] = selected_journey
        return response


class SelectSeatOfPassengerStepForSerializer(serializers.Serializer):
    pass


class SetFretStepFiveSerializer(serializers.Serializer):
    pass


class PayementStepSixSerializer(serializers.Serializer):
    pass


class ValideStepFinalSerializer(serializers.Serializer):
    pass
