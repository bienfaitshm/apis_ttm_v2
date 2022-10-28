from typing import TypedDict

from django.utils.translation import gettext_lazy as _


class InfoMessageJourneyTypedDict:
    j_number: str
    where_from: str
    where_to: str
    d_where_from: str
    h_where_from: str
    w_where_to: str
    d_where_to: str


class ErrorMessage:
    NOT_JOURNEY = _("not journey field")


class InfoJourneyMessage:
    default_message = "Voyage no {j_number}, Depart {where_from} le {d_where_from} a {h_where_from}, Arrive {where_to} le {d_where_to} a {w_where_to}"

    @classmethod
    def get_info_message(cls, *args, **kwargs) -> str:
        return cls.default_message.format(**kwargs)
