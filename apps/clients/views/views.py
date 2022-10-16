
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from xhtml2pdf import pisa

from utils import methods
from utils.pdf import pdf_link

from ..models import (
    FretPassenger, JourneySession, Passenger, PlaceReserved, SeletectedJourney,
)
from ..serializers import serialzers as sz


class TicketTemplateView(TemplateView):
    template_name = "clients/ticket_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # find the template and render it.

        template = get_template(self.template_name)
        html = template.render(context)

        print("Print====>")
        print(html)
        with open("pdf_ticket.pdf", "w+b") as result_file:
            # convert HTML to PDF
            pisa_status = pisa.CreatePDF(
                html,                # the HTML to convert
                dest=result_file
            )           # file handle to recieve result

        # # create a pdf
        # if pisa_status.err:  # type: ignore
        #     print("error")
        # context['code_confirmation'] = "https://www.google.com"
        return context


class FretPassengerView(viewsets.ModelViewSet):
    serializer_class = sz.FretPassengerSerializer
    queryset = FretPassenger.objects.all()


class PlaceReservedView(viewsets.ModelViewSet):
    serializer_class = sz.PlaceReservedSerializer
    queryset = PlaceReserved.objects.all()


class SeletectedJourneyView(viewsets.ModelViewSet):
    serializer_class = sz.SeletectedJourneySerializer
    queryset = SeletectedJourney.objects.all()\
        .select_related("session", "journey", "journey_class")
    # .prefetch_related("passengers")
    filter_backends = [
        DjangoFilterBackend
    ]

    filterset_fields = [
        'status',
        'pnr',
        'folder',
        'journey',
        'journey__dateDeparture',
        'journey__dateReturn',
        'journey_class',
        'session'
    ]

    def get_serializer_class(self):
        if self.action is methods.RETRIEVE:
            return sz.SeletectedJourneyMoreSerializer
        return super().get_serializer_class()


class JourneySessionView(viewsets.ModelViewSet):
    serializer_class = sz.JourneySessionSerializer
    queryset = JourneySession.objects.all()


class PassengerView(viewsets.ModelViewSet):
    serializer_class = sz.PassengerSerializer
    queryset = Passenger.objects.all()
