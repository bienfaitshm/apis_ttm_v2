from apps.dash.serializers import CabinePlaneSerializer
from datetime import datetime, timedelta
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
    FretPassengerSerializer, InputPassengerInfoStepThreeSerializer, JourneyClientFolderSerializer, JourneySessionSerializer,
    PassengerSerializer, PlaceReservedSerializer, SelectJourneyStepOneSerializer, SeletectedJourneySerializer, SetNumberOfPassengerStepTwoSerializer
)

SESSION_DAY = 2


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

    journey_selected_query_set = SeletectedJourney.objects.all()
    journey_session_query_set = JourneySession.objects.all()
    folder_query_set = JourneyClientFolder.objects.all()

    def get_step(self):
        return self.request.query_params.get(self.step_name_params)

    def get_session(self):
        return self.request.query_params.get(self.session_name_params)

    def get_folder(self):
        return self.request.query_params.get(self.folder_name_params)

    def check_session(self):
        step = self.get_step()
        session = self.get_session()
        folder = self.get_folder()
        if step is None and session is None:
            return
        else:
            checking_session = self.journey_session_query_set.filter(
                key=session
            )
            #
            if not checking_session.exists():
                raise exceptions.NotFound(
                    _(f"this session is not found '{session}'"))
            #
            session_instance = checking_session.first()
            print(session_instance)
            # if session_instance.dateExpiration < datetime.now():
            #     raise exceptions.PermissionDenied(
            #         _(f"pleace select a nother journey because this {session} session is exprired"))
            # #
            journey_instance = self.journey_selected_query_set.filter(
                folder__session=folder,
                session=session_instance
            )

            if not journey_instance.exists():
                raise exceptions.NotAcceptable(
                    _(f"{folder} is not accepatble or not containe this session"))

            journey_object = journey_instance.first()

            if journey_object.last_step < int(step) - 1:
                raise exceptions.NotAcceptable(
                    _("not allowed step"))
            return journey_object

    def init_reservation(self, journey=None):
        journey_instance = self.check_session()
        folder = self.get_folder()
        if journey_instance is None:
            session_instance = JourneySession.objects.create(
                key=get_random_key(),
                dateExpiration=datetime.today() + timedelta(days=SESSION_DAY)
            )
            instance = JourneyClientFolder.objects.filter(session=folder)
            if not instance.exists():
                folder_instance = JourneyClientFolder.objects.create(
                    number=get_random_key(10),
                    session=get_random_key()
                )
            else:
                folder_instance = instance.first()

            return SeletectedJourney.objects.create(
                folder=folder_instance,
                journey_id=journey,
                session=session_instance
            )
        return journey_instance

    def get_serializer_class(self):
        step = self.get_step()
        if step is not None:
            try:
                step = int(step)
                if step == 2:
                    return SetNumberOfPassengerStepTwoSerializer, self.action_of_step_two
                if step == 3:
                    return InputPassengerInfoStepThreeSerializer, self.action_of_step_three
            except:
                raise exceptions.APIException(
                    _("step is not connized"), code=status.HTTP_400_BAD_REQUEST)
        else:
            return SelectJourneyStepOneSerializer, self.action_of_step_one

    def action_of_step_one(self, serializer):
        serializer2 = serializer(data=self.request.data)
        serializer2.is_valid(raise_exception=True)
        result = self.init_reservation(
            journey=serializer2.validated_data.get("journey"))
        return Response({
            "selected": SeletectedJourneySerializer(result).data,
            "session": result.session.key,
            "folder": result.folder.session
        })

    def action_of_step_two(self, serializer):
        reserve = self.init_reservation()
        serializer2 = serializer(reserve, data=self.request.data, partial=True)
        serializer2.is_valid(raise_exception=True)
        result = serializer2.save()
        return Response({
            "selected": SeletectedJourneySerializer(result).data,
        })

    def action_of_step_three(self, serializer):
        journey = self.init_reservation()
        serializer2 = serializer(data=self.request.data)
        serializer2.is_valid(raise_exception=True)
        result = serializer2.save()
        return Response({
            "passengers": result.data,
            "seats": CabinePlaneSerializer(journey.journey.cars.configCab).data
        })

    def list(self, request, *args, **kwargs):
        code = get_random_key()
        response = HttpResponse('Does Not Works')
        response.set_cookie("folder_session", code)
        return response

    def post(self, request, *args, **kwargs):
        serializer, action_of_step = self.get_serializer_class()
        return action_of_step(serializer=serializer)
