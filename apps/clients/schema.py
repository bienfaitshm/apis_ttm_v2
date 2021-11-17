

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

from utils.node import CustomNode

class Query(graphene.ObjectType):
    fret_passenger = CustomNode.Field(FretPassengerType)
    fret_passengers = DjangoFilterConnectionField(FretPassengerType)

    folder_client = CustomNode.Field(JourneyClientFolderType)
    folder_clients = DjangoFilterConnectionField(JourneyClientFolderType)

    journey_session = CustomNode.Field(JourneySessionType)
    journey_sessions = DjangoFilterConnectionField(JourneySessionType)

    passenger = CustomNode.Field(PassengerType)
    passengers = DjangoFilterConnectionField(PassengerType)

    place_reserved = CustomNode.Field(PlaceReservedType)
    place_reserveds = DjangoFilterConnectionField(PlaceReservedType)

    journey_selected = CustomNode.Field(SeletectedJourneyType)
    journey_selecteds = DjangoFilterConnectionField(SeletectedJourneyType)

class Mutation(graphene.ObjectType):
    # frets = FretPassengerMutation.Field()
    reserve_info_passengers = InputPassengerInfoStepThreeMutation.Field()
    # client_folder = JourneyClientFolderMutation.Field()
    # session = JourneySessionMutation.Field()
    passengers = PassengerMutation.Field()
    reserve_place = PlaceReservedMutation.Field()
    # select_journey_step1 = SelectJourneyStepOneMutation.Field()
    select_journey = SeletectedJourneyMutation.Field()
