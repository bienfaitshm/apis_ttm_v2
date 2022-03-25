from django.db import models
from django.utils.translation import gettext as _
import datetime
from apps.account.models import Company, Employe
from apps.dash.utils import get_routes_to_string
from utils.base_model import BaseModel
from apps.dash.models.technique import Cars
from utils.trajets import link_routes, get_routes, make_trajet

DEVISE = [
    ("CDF", "CDF"),
    ("USD", "USD")
]


class CoverCity(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="cities")
    town = models.CharField(_("cover city"), max_length=200)
    code = models.CharField(_("code"), max_length=200, null=True)
    latitude = models.FloatField(_("latitude"), null=True, default=None)
    longitude = models.FloatField(_("latitude"), null=True, default=None)

    def __str__(self) -> str:
        return f"{self.town}: #{self.pk}"


class Routing(BaseModel):
    company = models.ForeignKey(
        Company, related_name="routing", on_delete=models.CASCADE)
    whereFrom = models.ForeignKey(CoverCity, verbose_name=_(
        "where from"), on_delete=models.CASCADE, related_name="whereFrom")
    whereTo = models.ForeignKey(CoverCity, verbose_name=_(
        "where to"), on_delete=models.CASCADE, related_name="whereTo")

    def __str__(self) -> str:
        return f"{self.pk}: {self.whereFrom} -- {self.whereTo}"


class PointOfSale(BaseModel):
    company = models.ForeignKey(Company, verbose_name=_(
        "point-of-sale"), related_name="point_of_sale", on_delete=models.CASCADE)
    name = models.CharField(_("name"), max_length=200)
    town = models.ForeignKey(CoverCity, verbose_name=_(
        "town of sale"), related_name="town_pos", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class PointOfSaleWorker(BaseModel):
    company = models.ForeignKey(Company, verbose_name=_(
        "point-of-sale worker"), related_name="worker_saler", on_delete=models.CASCADE)
    worker = models.ForeignKey(Employe, verbose_name=_(
        "worker"), related_name="worker", on_delete=models.CASCADE)
    pointOfSale = models.ForeignKey(PointOfSale, verbose_name=_(
        "point-of-sale"), related_name="worker_pos", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.worker} {self.company}"


class Journey(BaseModel):
    company = models.ForeignKey(
        Company, related_name="journey", on_delete=models.CASCADE)
    numJourney = models.CharField(_("number of journey"), max_length=50)
    price = models.IntegerField(_("price"))
    devise = models.CharField(
        _("money devise"), max_length=5, choices=DEVISE, default="CDF")
    dateDeparture = models.DateField(_("date of departure"))
    dateReturn = models.DateField(_("date of departure"))
    hoursDeparture = models.TimeField(_("hours of departure"))
    hoursReturn = models.TimeField(_("hours of return"))
    cars = models.ForeignKey(Cars, verbose_name=_(
        "cars"), on_delete=models.CASCADE, related_name="cars_journies")
    # routing = models.ManyToManyField(
    #     Routing, verbose_name=_("routing"), related_name="routing_journies")

    routes = models.ManyToManyField(
        Routing,
        through='RouteJourney',
        through_fields=('journey', 'route'),
        verbose_name=_("routing"), related_name="routing_journies"
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.numJourney} {self.company}"

    @property
    def is_direct(self) -> bool:
        return self.routes.count() <= 1

    @property
    def trajets(self):
        routes = self.get_routes()
        return make_trajet(get_routes(link_routes(routes)))

    def get_routes(self):
        return self.routes.all()

    def get_journey_routes(self):
        if hasattr(self, "journey_routes"):
            return self.journey_routes.all()

    @property
    def exprired(self) -> bool:
        now = datetime.datetime.now()
        day_expired = self.dateDeparture > now.date()
        hours_expired = (self.hoursDeparture.hour > now.hour) and (
            self.hoursDeparture.nimute > now.nimute)
        return not (hours_expired and day_expired)

    def number_places_taken(self):
        if hasattr(self, "journey_seats"):
            return self.journey_seats.filter(seat__type="SEAT").count()
        return 0

    @property
    def route_names(self):
        routes = self.get_routes()
        route_name = get_routes_to_string(routes)
        return _("non route names") if route_name == "" else route_name


class RouteJourney(BaseModel):
    route = models.ForeignKey(Routing, verbose_name=_(
        "routes"), on_delete=models.CASCADE, related_name="routes")
    journey = models.ForeignKey(Journey, verbose_name=_(
        "journey"), on_delete=models.CASCADE, related_name="journey_routes")
    price = models.IntegerField(_("price"))
    devise = models.CharField(
        _("money devise"), max_length=5, choices=DEVISE, default="CDF")

    def __str__(self) -> str:
        return f"{self.pk} {self.route} : {self.journey}"

    def __str__(self) -> str:
        return f"{self.pk} {self.route} {self.journey}"
