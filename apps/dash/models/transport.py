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
    image = models.ImageField(_("picture of city"), null=True)
    latitude = models.FloatField(_("latitude"), null=True, default=None)
    longitude = models.FloatField(_("latitude"), null=True, default=None)

    def __str__(self) -> str:
        return f"{self.town}: #{self.pk}"


class Routing(BaseModel):
    company = models.ForeignKey(
        Company, related_name="routing", on_delete=models.CASCADE)
    node = models.ForeignKey(CoverCity, verbose_name=_(
        "Current CoverCity"), on_delete=models.CASCADE, related_name="route")
    whereFrom = models.ForeignKey("self", verbose_name=_(
        "where from"), on_delete=models.SET_DEFAULT, related_name="predecessor", null=True, default=None)
    whereTo = models.ForeignKey("self", verbose_name=_(
        "where to"), on_delete=models.SET_DEFAULT, related_name="successor", null=True, default=None)
    distance = models.FloatField(_("distance(Km)"), default=0.0)

    def __str__(self) -> str:
        return f"Node {self.node}"


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


class JourneyClass(BaseModel):
    code = models.CharField(verbose_name=_("code_class"), max_length=10)
    name = models.CharField(verbose_name=_("name_class"), max_length=10)
    company = models.ForeignKey(
        Company, related_name="journey_class", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name} : {self.code}'


class JourneyTarif(BaseModel):
    '''
        *prix hors taxe
        *la taxe
        *PttaxCofondu = pht + tx 
        *classe de reservations = (classe 1="C", classe 2="J", classe 3="D", classe 4="F")
        *classe_1(D): (routing -> l'shi - klz, )
            *adulte = (pdb + tx = pttc) =>(100fc + 30fc = 130fc)
            *child = (pdb + tx = pttc) =>(70fc + 30fc = 100fc)
            *baby  = (pdb + tx = pttc) =>(50fc + 30fc = 80fc)
            ----------------------------------------------------
        *class_2(J) :(routing -> l'shi - klz, )
            *adulte = (pdb + tx = pttc) =>(130fc + 30fc = 160fc)
            *child = (pdb + tx = pttc) =>(80fc + 30fc = 110fc)
            *baby  = (pdb + tx = pttc) =>(60fc + 30fc = 90fc)
            ----------------------------------------------------
        *class_4(F) :(routing -> l'shi - klz, )
            *adulte = (pdb + tx = pttc) =>(0fc + 30fc = 30fc)
            *child = (pdb + tx = pttc) =>(0fc + 30fc = 110fc)
            *baby  = (pdb + tx = pttc) =>(0fc + 30fc = 90fc)
            NB: "pour les agents c'est l'entreprise qui paye la taxe"
            ...
    '''
    journey_class = models.ForeignKey(
        JourneyClass, on_delete=models.CASCADE, related_name='tarif')
    route = models.ForeignKey(Routing, verbose_name=_(
        "routes"), on_delete=models.CASCADE, related_name="routes")
    devise = models.CharField(
        _("money devise"), max_length=5, choices=DEVISE, default="CDF")
    adult = models.FloatField(verbose_name=_('tarif_adult'), default=0.0)
    child = models.FloatField(verbose_name=_('tarif_child'), default=0.0)
    baby = models.FloatField(verbose_name=_('tarif_baby'), default=0.0)
    taxe = models.FloatField(verbose_name=_('taxe'), default=0.0)
    actif = models.BooleanField(verbose_name=_('actif_tarif'), default=True)

    def pttc_adulte(self) -> float:
        # prix toute taxe confondu adulte
        return self.adult + self.taxe

    def pttc_child(self) -> float:
        # prix toute taxe confondu adulte
        return self.child + self.taxe

    def pttc_baby(self) -> float:
        # prix toute taxe confondu adulte
        return self.baby + self.taxe


class Journey(BaseModel):
    company = models.ForeignKey(
        Company, related_name="journey", on_delete=models.CASCADE)
    numJourney = models.CharField(_("number of journey"), max_length=50)
    dateDeparture = models.DateField(_("date of departure"))
    dateReturn = models.DateField(_("date of departure"))
    hoursDeparture = models.TimeField(_("hours of departure"))
    hoursReturn = models.TimeField(_("hours of return"))
    cars = models.ForeignKey(Cars, verbose_name=_(
        "cars"), on_delete=models.CASCADE, related_name="cars_journies")
    route = models.ForeignKey(Routing, verbose_name=_(
        "routing"), on_delete=models.SET_DEFAULT, related_name="routing_journies", null=True, default=None)

    def __str__(self) -> str:
        return f"{self.pk} {self.numJourney} {self.company}"

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
