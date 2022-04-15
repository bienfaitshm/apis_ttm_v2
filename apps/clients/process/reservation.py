import string
from datetime import datetime
from django.utils.crypto import get_random_string

from apps.dash.models import JourneyClass
from apps.dash.models.transport import Journey

from ..models import SeletectedJourney, JourneyClientFolder, JourneySession


class ReservationJourney:
    @classmethod
    def select_journey(cls, *args, **kwargs):
        session = cls.get_session(cls)
        folder = cls.get_client_folder(cls)

        return SeletectedJourney.objects.create(
            session=session,
            folder=folder,
            **kwargs
        )

    def get_client_folder(self):
        return JourneyClientFolder.objects.create(
            number=get_random_string(4, string.digits),
            session=get_random_string(5, string.ascii_letters)
        )

    def get_session(self):
        return JourneySession.objects.create(
            key=get_random_string(10, string.ascii_letters),
            date_expiration=datetime.now()
        )
