from datetime import datetime
from typing import Literal, Union

from utils.base_model import PersonneGenderBase

TYPE_FORMAT = Union[Literal["time"], Literal["date"]]

DATE_FORMAT = "%A %d %B %Y"
TIME_FORMAT = "%H:%M"

FORMAT = {
    "time": TIME_FORMAT,
    "date": DATE_FORMAT
}

type_name = {
    PersonneGenderBase.MAN: "Mr",
    PersonneGenderBase.WOMAN: "Mme",
    PersonneGenderBase.INDERTEMINAT: "Mr/Mme"
}


def title_fullname(gender: str, fullname: str):
    title = type_name.get(gender, "Mr")
    return f"{title} {fullname}"


def stringfy_datetime(value: datetime, format: TYPE_FORMAT = "date") -> str:
    return value.strftime(FORMAT.get(format, DATE_FORMAT)) if hasattr(value, "strftime") else "-"
