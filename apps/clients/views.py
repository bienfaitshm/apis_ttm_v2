from django.http.response import HttpResponse
from utils.generate_code import get_random_key
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from django.utils.translation import gettext as _

from .models import (
    FretPassenger, JourneyClientFolder, PlaceReserved, SeletectedJourney,
    JourneySession, Passenger,
)
from .serialzers import(
    FretPassengerSerializer, JourneyClientFolderSerializer, JourneySessionSerializer,
    PassengerSerializer, PlaceReservedSerializer, SelectJourneyStepOneSerializer, SeletectedJourneySerializer
)


class FretPassengerView(viewsets.ModelViewSet):
    serializer_class = FretPassengerSerializer
    queryset = FretPassenger.objects.all()


class JourneyClientFolderView(viewsets.ModelViewSet):
    serializer_class = JourneyClientFolderSerializer
    queryset = JourneyClientFolder.objects.all()


class PlaceReservedView(viewsets.ModelViewSet):
    serializer_class = PlaceReservedSerializer
    queryset = PlaceReserved.objects.all()


class SeletectedJourneyView(viewsets.ModelViewSet):
    serializer_class = SeletectedJourneySerializer
    queryset = SeletectedJourney.objects.all()


class JourneySessionView(viewsets.ModelViewSet):
    serializer_class = JourneySessionSerializer
    queryset = JourneySession.objects.all()


class PassengerView(viewsets.ModelViewSet):
    serializer_class = PassengerSerializer
    queryset = Passenger.objects.all()


class ReservationWithSteperView(viewsets.ViewSet):
    step_name_params = "step"
    session_name_params = "session"
    folder_name_params = "folder"

    journey_selected = SeletectedJourney.objects.all()
    journey_session = JourneySession.objects.all()

    def get_step(self):
        return self.request.query_params.get(self.step_name_params)

    def get_session(self):
        return self.request.query_params.get(self.session_name_params)

    def get_folder(self):
        return self.request.query_params.get(self.folder_name_params)

    def check_session(self):
        pass

    def init_reservation(self):
        step = self.get_step()
        session = self.get_session()

    def get_serializer_class(self):
        step = self.get_step()
        if step == "1":
            return SelectJourneyStepOneSerializer, self.action_of_step_one
        raise exceptions.APIException(
            _("step not allowed"), code=status.HTTP_400_BAD_REQUEST)

    def action_of_step_one(self, serializer):
        request = self.request

        return Response({
            "selected": "bienfait"
        })

    def list(self, request, *args, **kwargs):
        code = get_random_key()
        response = HttpResponse('Does Not Works')
        response.set_cookie("folder_session", code)
        return response

    def post(self, request, *args, **kwargs):
        serializer, action_of_step = self.get_serializer_class()
        return action_of_step(serializer=serializer)
