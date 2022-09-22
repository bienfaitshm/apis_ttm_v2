
from typing import Any, Dict, List, Union

from django.db.models import QuerySet

from apps.dash.models import Journey, JourneyTarif, Routing


def finder_journey() -> Union[List[Any], List[Dict[str, Any]], QuerySet[Any]]:
    # sourcery skip: inline-immediately-returned-variable
    data = []
    routes = Routing.objects.all().values_list('id', flat=True)

    tarif = JourneyTarif.objects.filter(
        route__in=routes).select_related("route", "route__orgine")
    journies = Journey.objects.all()

    for tarif in tarif:
        print("tarif: ", tarif)
        print("route", tarif.route.orgine)

    for journey in journies:
        # print("route: ", journey.route)
        # print(" tarif: ", journey.route.tarif_routes)
        data.append(journey)
    return data
