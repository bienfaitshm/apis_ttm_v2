from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.pk}"


class PersonneGenderBase(models.Model):
    WOMAN = "F"
    MAN = "H"
    INDERTEMINAT = "I"
    _GENDERS = [
        (WOMAN, _("Woman")),
        (MAN, _("Man")),
        (INDERTEMINAT, _("Indeterminate")),
    ]
    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=10,
        choices=_GENDERS,
        default=INDERTEMINAT
    )

    class Meta:
        abstract = True


class PaymentBaseModel(BaseModel):
    USD = "USD"
    CDF = "DCF"
    _DEVISE = [
        (USD, _("Dollars")),
        (CDF, _("Franc congolais"))
    ]

    devise = models.CharField(
        max_length=5,
        choices=_DEVISE,
        default=CDF,
        verbose_name=_("Devise"),
        help_text=_("the kind of money"),
    )

    class Meta:
        abstract = True
