from datetime import datetime
from typing import TypedDict


class RCompletedDataType(TypedDict):
    booker: str
    expire_datetime: datetime
    pnr: str
    total_price: str
    text_reservation: str
    passengers: list
