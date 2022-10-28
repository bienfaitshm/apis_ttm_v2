from email.policy import default
from tabnanny import verbose

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models import Client, PersonalMixin
from apps.dash.models.technique import Seat
from apps.dash.models.transport import (
    CoverCity, Journey, JourneyClass, Routing,
)
from utils.base_model import BaseModel, PersonneGenderBase


class ResearchReservation(BaseModel):
    adult = models.IntegerField(
        _("number of adult"),
        default=1
    )
    child = models.IntegerField(
        _("number of child"),
        default=0
    )
    baby = models.IntegerField(
        verbose_name=_("number of baby"),
        default=0
    )
    dateDepart = models.DateField(
        verbose_name=_("Departure Date")
    )
    journey_class = models.ForeignKey(
        JourneyClass,
        verbose_name=_("journe's class"),
        on_delete=models.SET_NULL,
        null=True,
    )
    whereFrom = models.ForeignKey(
        CoverCity,
        verbose_name=_("where from"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="recherche_route_whereFrom"
    )
    whereTo = models.ForeignKey(
        CoverCity,
        verbose_name=_("where to"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="recherche_route_whereTo"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True
    )


class JourneyClientFolder(BaseModel):
    number = models.CharField(
        verbose_name=_("number folder"),
        unique=True,
        max_length=200
    )
    session = models.CharField(
        verbose_name=_("session"),
        max_length=200,
        blank=True,
        null=True,
        default=None
    )
    client = models.ForeignKey(
        Client,
        verbose_name=_("client"),
        related_name="folder",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.number


class JourneySession(BaseModel):
    key = models.CharField(
        verbose_name=_("key session folder"),
        unique=True,
        max_length=200
    )
    date_expiration = models.DateTimeField(
        verbose_name=_("expiration date")
    )

    def __str__(self):
        return self.key


class SeletectedJourney(BaseModel):
    OPTION = "OP"
    VOIDED = "VD"
    EMITED = "ES"
    RESERVAION_STATUS = [
        (OPTION, 'In option'),
        (VOIDED, "Voided"),
        (EMITED, "Emis")
    ]
    status = models.CharField(
        verbose_name=_('status reservation'),
        max_length=20,
        choices=RESERVAION_STATUS,
        default=OPTION
    )
    adult = models.IntegerField(
        verbose_name=_("number of adult"),
        default=1
    )
    child = models.IntegerField(
        verbose_name=_("number of child"),
        default=0
    )
    baby = models.IntegerField(
        verbose_name=_("number of baby"),
        default=0
    )
    pnr = models.CharField(
        verbose_name=_("Passenger name record"),
        max_length=7,
        unique=True,
        null=True
    )
    folder = models.ForeignKey(
        JourneyClientFolder,
        verbose_name=_("folder"),
        on_delete=models.CASCADE,
        related_name="reservations",
        null=True,
        default=None
    )
    journey = models.ForeignKey(
        Journey,
        verbose_name=_("journey"),
        on_delete=models.CASCADE,
        related_name="journey_selected"
    )
    session = models.OneToOneField(
        JourneySession,
        verbose_name=_("session"),
        on_delete=models.CASCADE,
        related_name="session_journey_selected"
    )
    journey_class = models.ForeignKey(
        JourneyClass,
        verbose_name=_("journe's class"),
        on_delete=models.SET_DEFAULT,
        default=None, null=True
    )

    @property
    def passenger_total(self) -> int:
        return self.adult + self.baby + self.child


class Passenger(PersonneGenderBase, PersonalMixin):
    ADULT = 'AD'
    CHILD = 'CHD'
    BABY = 'INF'
    _PASSENGER_TYPE = [
        (ADULT, _("Adult")),
        (CHILD, _("Child")),
        (BABY, _("Baby")),
    ]

    journey = models.ForeignKey(
        SeletectedJourney,
        verbose_name=_("journey"),
        on_delete=models.CASCADE,
        related_name="passengers"
    )

    typeUser = models.CharField(
        verbose_name=_("type of user"),
        max_length=20,
        choices=_PASSENGER_TYPE,
        default=ADULT
    )


class PlaceReserved(BaseModel):
    seat = models.ForeignKey(
        Seat,
        verbose_name=_("seat"),
        related_name="place_reseved",
        on_delete=models.CASCADE
    )
    passenger = models.ForeignKey(
        Passenger,
        verbose_name=_("passenger"),
        related_name="passengers",
        on_delete=models.CASCADE
    )
    expired = models.BooleanField(
        verbose_name=_("expiration"),
        default=False
    )
    journey = models.ForeignKey(
        Routing,
        verbose_name=_("routes journey"),
        on_delete=models.CASCADE,
        related_name="journey_seats_reserved"
    )


class FretPassenger(BaseModel):
    passenger = models.OneToOneField(
        Passenger,
        verbose_name=_("passenger"),
        related_name="frets",
        on_delete=models.CASCADE
    )
    poid = models.IntegerField(
        verbose_name=_("poids")
    )
    volume = models.IntegerField(
        verbose_name=_("volume")
    )
    code = models.CharField(
        verbose_name=_("code of fret"),
        max_length=50
    )

    def __str__(self) -> str:
        return f"{self.passenger} {self.code}"


class OtherInfoReservation(PersonneGenderBase, PersonalMixin):
    """
        other information of model
    """

    journey = models.OneToOneField(
        SeletectedJourney,
        verbose_name=_("reservations"),
        related_name="other_info",
        help_text=_("the selected journey reservations"),
        on_delete=models.CASCADE,
    )

    email = models.EmailField(_("email"), max_length=200)
    num_tel = models.CharField(_("num_tel"), max_length=200)
    num_tel_emergency = models.CharField(
        verbose_name=_("num_tel_emergency"),
        max_length=200
    )
    degre_parent = models.CharField(
        verbose_name=_("degre of parent"),
        max_length=200,
        help_text="degre of responsable of reservation",
        blank=True,
        null=True
    )
    piece_id = models.CharField(
        _("piece_id"),
        max_length=200,
        blank=True,
        null=True
    )
    num_piece_id = models.CharField(
        _("num_piece_id"),
        max_length=200,
        blank=True,
        null=True
    )
    adress_from = models.CharField(
        verbose_name=_("adress_from"),
        max_length=250,
        blank=True,
        null=True
    )
    adress_to = models.CharField(
        verbose_name=_("adress_to"),
        max_length=250,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f"{self.pk} - {self.fullname}"


class SendTicket(BaseModel):
    journey = models.OneToOneField(
        SeletectedJourney,
        verbose_name=_("reservations"),
        related_name="send_ticket",
        help_text=_("the selected journey reservations"),
        on_delete=models.CASCADE,
    )
    sended = models.BooleanField(
        verbose_name=("sended Ticket"),
        default=False
    )
    to = models.CharField(
        null=True,
        blank=True,
        max_length=200,
        verbose_name=("sended Ticket"),
    )

    def __str__(self) -> str:
        return f"sended {self.sended} to {self.to}"
