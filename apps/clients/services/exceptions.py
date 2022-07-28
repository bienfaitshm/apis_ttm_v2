from enum import Enum

from django.utils.translation import gettext_lazy as _


class ErrorExpection(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class MessageExpection:
    PASSENGERS_NO_ALLOWED = _(
        """
        the passengers don't have this reservation,
        passengers not allowed for spliting the reservation
        """)
    VOID_NO_ALLOWED = _("you can splite this voided reservation")
    IMPOSSIBLE = _("inpossible to splite, please try egain.")
