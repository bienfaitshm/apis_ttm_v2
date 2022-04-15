from rest_framework.routers import DefaultRouter
from django.urls import path

from .views.views import (
    PassengerView
)
from .views.reservation import SelectJourneyreservationView

router = DefaultRouter()
router.register(r'reservation/passenger', PassengerView, basename='passenger')


urlpatterns = [
    path("reservation/select", SelectJourneyreservationView.as_view(),
         name="select_journey")
]+router.urls
