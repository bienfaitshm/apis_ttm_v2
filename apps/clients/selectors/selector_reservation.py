from django.db import models

from django.db.models.functions import Concat
from ..models import SeletectedJourney, Passenger


def get_dash_reservations():
    return SeletectedJourney.objects.all()


def get_dash_detail_reservation():
    select_related = ("other_info", "journey", "journey_class",)
    prefetch_related = ("passengers",)

    client_full_name = models.ExpressionWrapper(
        Concat(
            models.F("other_info__firstname"),
            models.Value(" "),
            models.F("other_info__middlename"),
            models.Value(" "),
            models.F("other_info__lastname"),
        ),
        output_field=models.CharField(max_length=200)
    )

    return SeletectedJourney.objects\
        .select_related(*select_related)\
        .prefetch_related(*prefetch_related)\
        .annotate(
            client_full_name=client_full_name,
            n_folder=models.F("folder__number")
        )
