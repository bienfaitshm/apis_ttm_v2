from datetime import datetime
from typing import Any, List, Optional, TypedDict


class RCompletedDataType(TypedDict):
    booker: str
    expire_datetime: datetime
    pnr: str
    total_price: str
    text_reservation: str
    passengers: list


class RJourneyDataType(TypedDict):
    uid: int
    where_from: str
    where_to: str
    datetime_from: Any
    datetime_to: Any
    duration: Any
    j_class: str
    total_price: int
    device: str
    has_ascale: bool
    passengers: Optional[Any]
    scales: Optional[List[str]]
    message: Optional[str]
    is_selected_for: Optional[bool]
    is_expired: Optional[bool]
