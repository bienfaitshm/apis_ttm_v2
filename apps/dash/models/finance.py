from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext as _
from django.dispatch import receiver

from utils.base_model import BaseModel
from apps.clients.models import SeletectedJourney


class ValidationPayment(BaseModel):
    journey_selected = models.ForeignKey(
        SeletectedJourney,
        verbose_name=_("voyage selectionner"),
        related_name="payment"
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
def recevingaction_signale(sender, instance, created, **kwargs):
    if created:
        ValidationPayment.objects.create(
            journey_selected=instance,
        )
