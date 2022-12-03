from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.clients.views.actions import SplitFolderView, VoidSelectedJourneyView

from .views import views as ActionView
from .views.actions import ActionViewApis
from .views.reservation import ReservationViewApis

router = DefaultRouter()
router.register(
    prefix=r"reservations",
    viewset=ReservationViewApis,
    basename="reservations"
)

router.register(
    prefix=r"actions/reservations",
    viewset=ActionViewApis,
    basename="reservations_actions"
)

router.register(
    r"actions/reservations",
    ActionView.SeletectedJourneyView,
    basename="reservations2"
)
router.register(
    r'actions/passengers',
    ActionView.PassengerView,
    basename='passengers'
)


urlpatterns = [
    path(
        "actions/splite",
        SplitFolderView.as_view(),
        name="splite_folder"
    ),
    path(
        "actions/reservations/<id>/void/",
        VoidSelectedJourneyView.as_view(),
        name="void_folder"
    ),

    path("template/ticket", ActionView.TicketTemplateView.as_view())

]+router.urls
