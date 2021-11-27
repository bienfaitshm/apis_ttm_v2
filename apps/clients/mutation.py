import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from .serialzers import (
    FretPassengerSerializer, InputPassengerInfoStepThreeSerializer, JourneyClientFolderSerializer,
    JourneySessionSerializer, PayementStepSixSerializer, PlaceReservedSerializer,SelectJourneyStepOneSerializer,
    SelectSeatOfPassengerStepForSerializer,
    PassengerSerializer, SeletectedJourneySerializer, SetFretStepFiveSerializer, SetNumberOfPassengerStepTwoSerializer,
    ValideStepFinalSerializer, OtherInfoReservationSerializer, ValidationPaymentSerializer
)

class FretPassengerMutation(SerializerMutation):
    class Meta:
        serializer_class =FretPassengerSerializer
        # exclude_fields = ["pub_type","visibility"]

class FretPassengerMutation(SerializerMutation):
    class Meta:
        serializer_class =FretPassengerSerializer

class OtherInfoReservationMutation(SerializerMutation):
    class Meta:
        serializer_class =OtherInfoReservationSerializer
        exclude_fields = ["gender",]

class ValidationPaymentMutation(SerializerMutation):
    class Meta:
        serializer_class = ValidationPaymentSerializer
class FretPassengerMutation(SerializerMutation):
    class Meta:
        serializer_class =FretPassengerSerializer

class InputPassengerInfoStepThreeMutation(SerializerMutation):
    class Meta:
        serializer_class = InputPassengerInfoStepThreeSerializer
        # exclude_fields = ["pub_type","visibility"]

class JourneyClientFolderMutation(SerializerMutation):
    class Meta:
        serializer_class = JourneyClientFolderSerializer
        # exclude_fields = ["pub_type","visibility"]

class JourneySessionMutation(SerializerMutation):
    class Meta:
        serializer_class = JourneySessionSerializer
        # exclude_fields = ["pub_type","visibility"]
        #
class PayementStepSixMutation(SerializerMutation):
    class Meta:
        serializer_class = PayementStepSixSerializer
        # exclude_fields = ["pub_type","visibility"]
         
class PlaceReservedMutation(SerializerMutation):
    class Meta:
        serializer_class = PlaceReservedSerializer
        # exclude_fields = ["pub_type","visibility"]

class SelectJourneyStepOneMutation(SerializerMutation):
    class Meta:
        serializer_class = SelectJourneyStepOneSerializer
        
class SelectSeatOfPassengerStepForMutation(SerializerMutation):
    class Meta:
        serializer_class = SelectSeatOfPassengerStepForSerializer

class PassengerMutation(SerializerMutation):
    class Meta:
        serializer_class = PassengerSerializer
        exclude_fields = ["gender","typeUser"]

class SeletectedJourneyMutation(SerializerMutation):
    class Meta:
        serializer_class = SeletectedJourneySerializer

class SetFretStepFiveMutation(SerializerMutation):
    class Meta:
        serializer_class = SetFretStepFiveSerializer

class SetNumberOfPassengerStepTwoMutation(SerializerMutation):
    class Meta:
        serializer_class = SetNumberOfPassengerStepTwoSerializer

class ValideStepFinalMutation(SerializerMutation):
    class Meta:
        serializer_class = ValideStepFinalSerializer
