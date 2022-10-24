from django.db import models
from django.utils.translation import gettext as _

from apps.account.models import Company
from utils.base_model import BaseModel


class SeatConfig(BaseModel):
    SEAT = "SEAT"
    SPACE = "SPACE"
    TYPE_SEAT = [
        (SEAT, 'seating'),
        (SPACE, 'space or  couloir')
    ]

    class Meta:
        abstract = True


class CabinePlane(SeatConfig):

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="cabine_plane")
    name = models.CharField(default="nameDefaultConfig", max_length=256)
    devMod = models.BooleanField(default=False)
    x = models.IntegerField(
        help_text="configuration in x or the total number of line seat")
    y = models.IntegerField(
        help_text="configuration in y or the total of column of seats")
    clipboard = models.CharField(
        choices=SeatConfig.TYPE_SEAT, max_length=10, default=SeatConfig.SEAT)

    def __str__(self):
        return f"{self.name} {self.pk}"


class Seat(SeatConfig):

    idConfigCab = models.ForeignKey(
        CabinePlane, on_delete=models.CASCADE, related_name="seats")
    name = models.CharField(_("name"), max_length=50)
    type = models.CharField(
        _("type"),
        max_length=10,
        choices=SeatConfig.TYPE_SEAT,
        default=SeatConfig.SEAT
    )
    x = models.IntegerField(_("x"))
    y = models.IntegerField(_("y"))

    def __str__(self) -> str:
        return f"{self.pk} {self.idConfigCab} {self.name}"


class Cars(BaseModel):
    OPERATIONAL = "OP"
    NON_OPERATIONAL = "NO"
    OUT_SERVICE = "HS"

    ETAT_APPARAIL = [
        (OPERATIONAL, "Operationnel"),
        (NON_OPERATIONAL, "Non operationnel"),
        (OUT_SERVICE, "Hors service")
    ]
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="pompany_cars")
    configCab = models.ForeignKey(
        CabinePlane, on_delete=models.CASCADE, related_name="cars")
    typeAppareil = models.CharField(max_length=200)
    indexKm = models.CharField(max_length=200)
    immatriculation = models.CharField(max_length=200)
    codeAppareil = models.CharField(max_length=200)
    etat = models.CharField(
        max_length=10,
        choices=ETAT_APPARAIL,
        default=OPERATIONAL
    )
    miseEnService = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.immatriculation} : {self.typeAppareil}"
