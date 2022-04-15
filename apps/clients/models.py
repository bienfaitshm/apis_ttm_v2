from django.db import models
from django.utils.translation import gettext as _

from utils.base_model import BaseModel
from apps.account.models import Client, PersonalMixin
from apps.dash.models.technique import Seat
from apps.dash.models.transport import Journey, Routing

from django.db.models.signals import post_save
from django.dispatch import receiver


class JourneyClientFolder(BaseModel):
    number = models.CharField(_("number folder"), unique=True, max_length=200)
    session = models.CharField(
        _("session"), max_length=200, blank=True, null=True, default=None)
    client = models.ForeignKey(
        Client, verbose_name=_("client"), related_name="folder", on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.number


class JourneySession(BaseModel):
    key = models.CharField(_("key session folder"),
                           unique=True, max_length=200)
    date_expiration = models.DateTimeField(_("expiration date"))

    def __str__(self) -> str:
        return self.key


class SeletectedJourney(BaseModel):
    folder = models.ForeignKey(JourneyClientFolder, verbose_name=_(
        "folder"), on_delete=models.CASCADE, related_name="folder_journey_selected")
    journey = models.ForeignKey(Journey, verbose_name=_(
        "journey"), on_delete=models.CASCADE, related_name="journey_selected")
    session = models.OneToOneField(JourneySession, verbose_name=_(
        "session"), on_delete=models.CASCADE, related_name="session_journey_selected")
    adult = models.IntegerField(_("number of adult"), default=1)
    child = models.IntegerField(_("number of child"), default=0)
    baby = models.IntegerField(_("number of baby"), default=0)

    @property
    def journey_class(self):
        return 2


class Passenger(PersonalMixin):
    TYPE = [
        ("adult", _("Adult")),
        ("child", _("Child")),
        ("baby", _("Baby")),
    ]

    GENDERS = [
        ("F", _("Woman")),
        ("H", _("Man")),
        ("I", _("Indeterminate")),
    ]

    journey = models.ForeignKey(SeletectedJourney, verbose_name=_(
        "journey"), on_delete=models.CASCADE, related_name="passengers")
    gender = models.CharField(_("gender"), max_length=10, choices=GENDERS)
    typeUser = models.CharField(_("type of user"), max_length=20, choices=TYPE)


class PlaceReserved(BaseModel):
    seat = models.ForeignKey(Seat, verbose_name=_(
        "seat"), related_name="place_reseved", on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, verbose_name=_(
        "passenger"), related_name="passengers", on_delete=models.CASCADE)
    expired = models.BooleanField(_("expiration"), default=False)
    journey = models.ForeignKey(Routing, verbose_name=_(
        "routes journey"), on_delete=models.CASCADE, related_name="journey_seats_reserved")


class FretPassenger(BaseModel):
    passenger = models.OneToOneField(Passenger, verbose_name=_(
        "passenger"), related_name="frets", on_delete=models.CASCADE)
    poid = models.IntegerField(_("poids"))
    volume = models.IntegerField(_("volume"))
    code = models.CharField(_("code of fret"), max_length=50)

    def __str__(self) -> str:
        return f"{self.passenger} {self.code}"


class OtherInfoReservation(PersonalMixin):
    """
        other information of model
    """
    GENDERS = [
        ("F", _("Woman")),
        ("H", _("Man")),
        ("I", _("Indeterminate")),
    ]
    journey = models.OneToOneField(
        SeletectedJourney,
        verbose_name=_("reservations"),
        on_delete=models.CASCADE,
        related_name="other_info",
        help_text=_("the selected journey reservations")
    )

    gender = models.CharField(_("gender"), max_length=10, choices=GENDERS)
    email = models.EmailField(_("name"), max_length=200)
    num_tel = models.CharField(_("name"), max_length=200)
    num_tel_emergency = models.CharField(_("name"), max_length=200)
    degre_parent = models.CharField(
        _("degre of parent"), max_length=200, help_text="degre of responsable of reservation")
    piece_id = models.CharField(_("name"), max_length=200)
    num_piece_id = models.CharField(_("name"), max_length=200)
    adress_from = models.CharField(_("name"), max_length=250)
    adress_to = models.CharField(_("name"), max_length=250)

    def __str__(self):
        return f"{self.pk} {self.firstname}"

    def get_full_name(self):
        return f"{self.firstname} {self.middlename} {self.lastname}"


class ValidationPayment(BaseModel):
    journey_selected = models.OneToOneField(
        SeletectedJourney,
        verbose_name=_("voyage selectionner"),
        related_name="payment",
        on_delete=models.CASCADE
    )
    provider = models.CharField(max_length=200, verbose_name="provider", help_text=_(
        "provider determine the mode of payment"), default="CASH")
    confirmed = models.BooleanField(
        verbose_name=_("confirmation"), default=False)
    costTotal = models.CharField(max_length=200, null=True)
    date_payment = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.costTotal} {self.confirmed}"


@receiver(post_save, sender=SeletectedJourney)
def creation_validation_signal(sender, instance, created, **kwargs):
    """
        the signal to automatise the creation of Validation of payment!
    """
    if created:
        ValidationPayment.objects.create(
            journey_selected=instance,
        )
