from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    PassengerView, FretPassengerView, PlaceReservedView, JourneySessionView, SeletectedJourneyView,
    JourneyClientFolderView, ReservationWithSteperView
)

router = DefaultRouter()
router.register(r'passenger', PassengerView, basename='passenger')
router.register(r'fret_client', FretPassengerView, basename='fret_client')
router.register(r'place_reserved', PlaceReservedView,
                basename='place_reserved')
router.register(r'jrny_session', JourneySessionView, basename='jrny_session')
router.register(r'selected_jrny', SeletectedJourneyView,
                basename='selected_jrny')
router.register(r'jrny_client_folder', JourneyClientFolderView,
                basename='jrny_client_folder')

urlpatterns = [
    path("reserve/", ReservationWithSteperView.as_view({
        'get': 'list'
    }))
]+router.urls
