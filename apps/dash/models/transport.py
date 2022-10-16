
import time

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import Company, Employe
from apps.dash.models import managers
from apps.dash.models.technique import Cars
from utils import times as utils_time
from utils.base_model import BaseModel, PaymentBaseModel


class CoverCity(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="cities"
    )
    town = models.CharField(
        _("cover city"),
        max_length=200
    )
    code = models.CharField(
        _("code"),
        max_length=200,
        null=True
    )
    image = models.ImageField(
        _("picture of city"),
        null=True
    )
    latitude = models.FloatField(
        _("latitude"),
        null=True,
        default=None
    )
    longitude = models.FloatField(
        _("latitude"),
        null=True,
        default=None
    )

    def __str__(self) -> str:
        return f"{self.town}: #{self.pk}"


class Routing(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name="routing",
        on_delete=models.CASCADE
    )
    node = models.ForeignKey(
        CoverCity,
        verbose_name=_("Current CoverCity"),
        on_delete=models.CASCADE,
        related_name="route"
    )
    whereFrom = models.ForeignKey(
        "self",
        verbose_name=_("where from"),
        on_delete=models.SET_DEFAULT,
        related_name="predecessor",
        null=True, default=None
    )
    whereTo = models.ForeignKey(
        "self",
        verbose_name=_("where to"),
        related_name="successor",
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    origin = models.ForeignKey(
        "self",
        verbose_name=_("origin"),
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        help_text=_("the orgin of routing(first town)")
    )

    level = models.IntegerField(
        default=0,
        help_text=_("level of deeper of route")
    )

    distance = models.FloatField(
        _("distance(Km)"),
        default=0.0
    )

    def __str__(self) -> str:
        return f"pk {self.pk } : Node {self.node}"


class PointOfSale(BaseModel):
    """ point of sale  """
    company = models.ForeignKey(
        Company,
        verbose_name=_("point-of-sale"),
        related_name="point_of_sale",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=200
    )
    town = models.ForeignKey(
        CoverCity,
        verbose_name=_("town of sale"),
        related_name="town_pos",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.name


class PointOfSaleWorker(BaseModel):
    company = models.ForeignKey(
        Company,
        verbose_name=_("point-of-sale worker"),
        related_name="worker_saler",
        on_delete=models.CASCADE
    )
    worker = models.ForeignKey(
        Employe,
        verbose_name=_("worker"),
        related_name="worker",
        on_delete=models.CASCADE
    )
    pointOfSale = models.ForeignKey(
        PointOfSale,
        verbose_name=_("point-of-sale"),
        related_name="worker_pos",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.worker} {self.company}"


class JourneyClass(BaseModel):
    code = models.CharField(
        verbose_name=_("code_class"),
        max_length=10
    )
    name = models.CharField(
        verbose_name=_("name_class"),
        max_length=10
    )
    company = models.ForeignKey(
        Company,
        related_name="journey_class",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.name} : {self.code}'


class JourneyTarif(PaymentBaseModel):
    """
    """
    USD = "USD"
    CDF = "CDF"
    DEVISES = [
        (USD, _("Dollars")),
        (CDF, _("Franc congolais"))
    ]

    devise = models.CharField(
        choices=DEVISES,
        default=CDF,
        max_length=10
    )
    journey_class = models.ForeignKey(
        JourneyClass,
        on_delete=models.CASCADE,
        related_name='tarif'
    )
    route = models.ForeignKey(
        Routing,
        verbose_name=_("routes"),
        on_delete=models.CASCADE,
        related_name="tarif_routes"
    )

    adult = models.FloatField(
        verbose_name=_('tarif_adult'),
        default=0.0
    )
    child = models.FloatField(
        verbose_name=_('tarif_child'),
        default=0.0
    )
    baby = models.FloatField(
        verbose_name=_('tarif_baby'),
        default=0.0
    )

    taxe = models.FloatField(
        verbose_name=_('taxe'),
        default=0.0
    )
    actif = models.BooleanField(
        verbose_name=_('actif_tarif'),
        default=True
    )

    def __str__(self) -> str:
        return f"{self.pk}"


class Journey(BaseModel):
    company = models.ForeignKey(
        Company,
        related_name="journey",
        on_delete=models.CASCADE
    )
    numJourney = models.CharField(
        verbose_name=_("number of journey"),
        max_length=50
    )
    dateDeparture = models.DateField(
        verbose_name=_("date of departure")
    )
    dateReturn = models.DateField(
        verbose_name=_("date of departure")
    )
    hoursDeparture = models.TimeField(
        verbose_name=_("hours of departure")
    )
    hoursReturn = models.TimeField(
        verbose_name=_("hours of return")
    )
    cars = models.ForeignKey(
        Cars,
        verbose_name=_("cars"),
        related_name="cars_journies",
        on_delete=models.CASCADE,
    )
    route = models.ForeignKey(
        Routing,
        verbose_name=_("routing"),
        null=True,
        default=None,
        related_name="routing_journies",
        on_delete=models.SET_DEFAULT,
    )

    # managers
    objects = managers.JourneyManager()

    def __str__(self) -> str:
        return f"{self.pk} {self.numJourney}"

    @property
    def is_expired(self) -> bool:
        return utils_time.is_expired(self.datetime_from)

    @property
    def duration(self):
        duration = (
            self.datetime_to - self.datetime_from
        ).total_seconds()
        return time.strftime("%H:%M",
                             time.gmtime(duration)) if duration > 0 else "-"

    @property
    def datetime_from(self) -> datetime:
        return utils_time.cobine_date_n_time(
            date=self.dateDeparture,
            time=self.hoursDeparture
        )

    @property
    def datetime_to(self) -> datetime:
        return utils_time.cobine_date_n_time(
            date=self.dateReturn,
            time=self.hoursReturn
        )
