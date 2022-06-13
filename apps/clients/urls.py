from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.clients.views.actions import SplitFolderView, VoidSelectedJourneyView

from .views import views as ActionView
from .views.reservation import (
    SelectJourneyreservationView, PassengerJourneyReservationView, OtherInfoReservationView, ReachercheJourneyReservationView)

router = DefaultRouter()
router.register(r'actions/folder',
                ActionView.JourneyClientFolderView, basename='folder')
router.register(r"actions/reservations",
                ActionView.SeletectedJourneyView, basename="reservations")
router.register(r'actions/passengers',
                ActionView.PassengerView, basename='passengers')


urlpatterns = [
    path("actions/splite", SplitFolderView.as_view(), name="splite_folder"),
    path("actions/reservations/<id>/void/",
         VoidSelectedJourneyView.as_view(), name="void_folder"),
    path("reservation/search/", ReachercheJourneyReservationView.as_view(),
         name="search_journey_reservation"),
    path("reservation/select/", SelectJourneyreservationView.as_view(),
         name="select_journey"),
    path("reservation/passengers/", PassengerJourneyReservationView.as_view(),
         name="passengers_journey"),
    path("reservation/other_info/", OtherInfoReservationView.as_view(),
         name="other_info_journey"),
]+router.urls
