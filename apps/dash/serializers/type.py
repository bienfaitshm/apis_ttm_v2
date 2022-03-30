
from typing import List, TypedDict


class RouteJourneyDataType(TypedDict):
    price: int
    devise: str
    route: int
    journey: int


class JourneyDataType(TypedDict):
    numJourney: str
    price: int
    devise: str
    dateDeparture: str
    dateReturn: str
    hoursDeparture: str
    hoursReturn: str
    company: int
    cars: int
    journey_routes: List[RouteJourneyDataType]
