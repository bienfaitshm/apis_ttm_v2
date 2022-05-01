
from apps.dash.models import JourneyTarif


def get_tarif_for_a_reservation(route, journey_class):
    """
    """
    try:
        d = JourneyTarif.objects.filter(
            journey_class=journey_class, route=route)
        if d.exists():
            return d.first()
    except JourneyTarif.DoesNotExist:
        pass
    return
