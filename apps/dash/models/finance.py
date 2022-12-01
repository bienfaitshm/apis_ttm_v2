
from django.db import models
from django.utils.translation import gettext as _

from apps.clients.models import Passenger
from utils.base_model import PaymentBaseModel

__all__ = ["Ticket", ]


class Ticket(PaymentBaseModel):
    OPTION = "OP"
    EMIS = "ES"
    NO_SHOW = "NS"
    VOID = "VD"
    FLOWN = "FN"
    STATUS = [
        (OPTION, _("In Option")),
        (EMIS, _("Emis")),
        (NO_SHOW, _("No-show")),
        (VOID, _("Voided")),
        (FLOWN, _("Flown"))
    ]
    status = models.CharField(
        verbose_name=_("status"),
        max_length=5,
        choices=STATUS,
        default=OPTION,
        help_text=_("status of ticked")
    )
    n_ticket = models.IntegerField(
        verbose_name=_("number of ticket"),
        unique=True
    )
    n_coupons = models.CharField(
        verbose_name=_("number of coupons"),
        max_length=20,
        blank=True,
        null=True,
        default=None
    )
    price = models.FloatField(
        verbose_name=_("price"),
        help_text=_("the price of thing"),
        default=0.0
    )

    passenger = models.OneToOneField(
        Passenger, on_delete=models.CASCADE,
        related_name="passenger_ticket",
        verbose_name=_("passenger"),
        help_text="the passenger to have this ticket"
    )

    class Meta:
        db_table = "tb_tickets"
        verbose_name = _("Billet")
        verbose_name_plural = _("Billets")
