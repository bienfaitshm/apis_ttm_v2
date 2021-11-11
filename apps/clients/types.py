import graphene
from graphene_django import DjangoObjectType
import datetime
from utils import node
from utils.user_mixin import UserMixin
from .models import (
    JourneyClientFolder, JourneySession, SeletectedJourney, 
    Passenger, PlaceReserved, FretPassenger
)

class JourneyClientFolderType(UserMixin, DjangoObjectType):
    class Meta:
        model = JourneyClientFolder
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class JourneySessionType(UserMixin, DjangoObjectType):
    class Meta:
        model = JourneySession
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"
    
class SeletectedJourneyType(UserMixin, DjangoObjectType):
    class Meta:
        model = SeletectedJourney
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class PassengerType(UserMixin, DjangoObjectType):
    class Meta:
        model = Passenger
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"

class PlaceReservedType(UserMixin, DjangoObjectType):
    class Meta:
        model = PlaceReserved
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"


class FretPassengerType(UserMixin, DjangoObjectType):
    class Meta:
        model = FretPassenger
        interfaces = (node.CustomNode,)
        filter_fields = []
        fields = "__all__"