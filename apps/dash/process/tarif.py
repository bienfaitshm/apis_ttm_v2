
from ..models import JourneyTarif


def get_tarif_of_route(route: int):
    return JourneyTarif.objects.filter(actif=True, route=route)
