from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import view_reservations as VR
from .views.routes import RouteProcessView
from .views.views import (
    CabinePlaneView, CarsView, CoverCityView, JourneyClassView,
    JourneyTarifView, JourneyView, PointOfSaleView, PointOfSaleWorkerView,
    RoutingView, SeatView,
)

router = DefaultRouter()
router.register(
    r'technic/cars',
    CarsView,
    basename='cars'
)
router.register(
    r'technic/seat',
    SeatView,
    basename='seat'
)
router.register(
    r'transport/classe',
    JourneyClassView,
    basename='classes'
)
router.register(
    r'transport/tarif',
    JourneyTarifView,
    basename='tarif'
)
router.register(
    r'transport/journey',
    JourneyView,
    basename='journey'
)
router.register(
    r'transport/routing',
    RoutingView,
    basename='routing'
)
router.register(
    r'transport/cover_city',
    CoverCityView,
    basename='cover_city'
)
router.register(
    r'transport/pos',
    PointOfSaleView,
    basename='point_of_sale'
)
router.register(
    r'transport/routes',
    RouteProcessView,
    basename='route'
)
router.register(
    r'technic/cabine_plane',
    CabinePlaneView,
    basename='cabine_plane'
)
router.register(
    r'transport/pos_worker',
    PointOfSaleWorkerView,
    basename='point_of_sale_worker'
)

urlpatterns = router.urls + [
    path(
        "dash/reservation",
        VR.DashViewReservation.as_view(),
        name="dash_reservation"
    ),
    path(
        "dash/reservation/<int:id>",
        VR.DashViewDetailReservation.as_view(),
        name="dash_detail_reservation"
    ),

    path(
        "search/journey",
        VR.JourneyFinder.as_view(),
        name="dash_detail_reservation"
    ),
]
