from django.db import models
from utils.base_model import BaseModel
from django.utils.translation import gettext as _
from apps.account.models import Company


class CabinePlane(BaseModel):
    TYPE_SEAT = [
        ('SEAT', 'seating'),
        ('SPACE', 'space or  couloir')
    ]
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="cabine_plane")
    name = models.CharField(default="nameDefaultConfig", max_length=256)
    devMod = models.BooleanField(default=False)
    x = models.IntegerField(
        help_text="configuration in x or the total number of line seat")
    y = models.IntegerField(
        help_text="configuration in y or the total of column of seats")
    clipboard = models.CharField(
        choices=TYPE_SEAT, max_length=10, default="SEAT")

    def __str__(self):
        return f"{self.name} {self.pk}"

    @property
    def number_of_seats(self):
        if hasattr(self,"seats"):
            return self.seats.filter(type = "SEAT").count()
        return 0


class Seat(BaseModel):
    TYPE = [
        ("SEAT", "SEAT"),
        ("SPACE", "SPACE")
    ]
    idConfigCab = models.ForeignKey(
        CabinePlane, on_delete=models.CASCADE, related_name="seats")
    name = models.CharField(_("name"), max_length=50)
    type = models.CharField(_("type"), max_length=10, choices=TYPE)
    x = models.IntegerField(_("x"))
    y = models.IntegerField(_("y"))

    def __str__(self) -> str:
        return f" {self.pk} {self.idConfigCab} {self.name}"
    
    def get_seats(self):
        return self.objects.filter(type="SEAT")
    
    @property
    def number_of_seats(self):
        return self.get_seats().count()
    
    def __str__(self) -> str:
        return f"{self.idConfigCab} {self.type} {self.pk}"


class Cars(BaseModel):
    ETAT_APPARAIL = [
        ("OP", "Operationnel"),
        ("NO", "Non operationnel"),
        ("HS", "Hors service")
    ]
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="pompany_cars")
    configCab = models.ForeignKey(
        CabinePlane, on_delete=models.CASCADE, related_name="cars")
    typeAppareil = models.CharField(max_length=200)
    indexKm = models.CharField(max_length=200)
    immatriculation = models.CharField(max_length=200)
    codeAppareil = models.CharField(max_length=200)
    etat = models.CharField(max_length=10, choices=ETAT_APPARAIL)
    miseEnService = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.immatriculation} : {self.typeAppareil}"
