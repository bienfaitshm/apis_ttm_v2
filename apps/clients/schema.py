

import graphene
from graphene import relay
from graphene_django.filter.fields import DjangoFilterConnectionField

from .types import (
    FretPassengerType, JourneyClientFolderType, JourneySessionType,
    PassengerType, PlaceReservedType, SeletectedJourneyType
)

from .mutation import (
    FretPassengerMutation, InputPassengerInfoStepThreeMutation,JourneyClientFolderMutation,
    JourneySessionMutation, PassengerMutation,PayementStepSixMutation,PlaceReservedMutation,
    SelectJourneyStepOneMutation, SelectSeatOfPassengerStepForMutation, SeletectedJourneyMutation,
    SetFretStepFiveMutation,ValideStepFinalMutation
)

class Query(graphene.ObjectType):
    fret_passenger = relay.Node.Field(FretPassengerType)
    fret_passengers = DjangoFilterConnectionField(FretPassengerType)

    folder_client = relay.Node.Field(JourneyClientFolderType)
    folder_clients = DjangoFilterConnectionField(JourneyClientFolderType)

    journey_session = relay.Node.Field(JourneySessionType)
    journey_sessions = DjangoFilterConnectionField(JourneySessionType)

    passenger = relay.Node.Field(PassengerType)
    passengers = DjangoFilterConnectionField(PassengerType)

    place_reserved = relay.Node.Field(PlaceReservedType)
    place_reserveds = DjangoFilterConnectionField(PlaceReservedType)

    journey_selected = relay.Node.Field(SeletectedJourneyType)
    journey_selecteds = DjangoFilterConnectionField(SeletectedJourneyType)

class Mutation(graphene.ObjectType):
    frets = FretPassengerMutation.Field()
    step_3 = InputPassengerInfoStepThreeMutation.Field()
    client_folder = JourneyClientFolderMutation.Field()
    session = JourneySessionMutation.Field()
    passenger = PassengerMutation.Field()
    payment_step6 = PayementStepSixMutation.Field()
    reserve_place = PlaceReservedMutation.Field()
    select_journey_step1 = SelectJourneyStepOneMutation.Field()
    select_passenger_seat = SelectSeatOfPassengerStepForMutation.Field()
    select_journey = SeletectedJourneyMutation.Field()
    setp5 = SetFretStepFiveMutation.Field()
    setp_final = ValideStepFinalMutation.Field()