from rest_framework.routers import DefaultRouter
from django.urls import path

from .views.views import (
    PassengerView
)
from .views.reservation import SelectJourneyreservationView, PassengerJourneyReservationView, OtherInfoReservationView

router = DefaultRouter()
router.register(r'reservation/passenger', PassengerView, basename='passenger')


urlpatterns = [
    path("reservation/select/", SelectJourneyreservationView.as_view(),
         name="select_journey"),
    path("reservation/passengers/", PassengerJourneyReservationView.as_view(),
         name="passengers_journey"),
    path("reservation/other_info/", OtherInfoReservationView.as_view(),
         name="other_info_journey"),
]+router.urls
