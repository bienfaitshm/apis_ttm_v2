"""
    _summary_
"""

from dataclasses import dataclass
from typing import Protocol


class IPriceSystem(Protocol):
    def get_ptt_adult(self) -> float: ...
    def get_ptt_child(self) -> float: ...
    def get_ptt_inf(self) -> float: ...
    def get_total_price(self) -> float: ...

    def set_passenger(self, *args, **kwargs) -> None: ...
    def set_tarif(self, *args, **kwargs) -> None: ...


@dataclass
class PriceSystem(IPriceSystem):
    adult: int = 1
    child: int = 0
    inf: int = 0

    taxe: float = 0
    adult_price: float = 0
    child_price: float = 0
    inf_price: float = 0

    def setter(self, *args, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_passenger(self, *args, **kwargs) -> None:
        self.setter(*args, **kwargs)

    def set_tarif(self, *args, **kwargs) -> None:
        self.setter(*args, **kwargs)

    def ppt(self, unit_price: float, taxe: float):
        """ prix toute taxe confondu """
        return unit_price * ((taxe / 100) + 1)

    def get_ptt_adult(self) -> float:
        return self.ppt(taxe=self.taxe, unit_price=self.adult_price)

    def get_ptt_child(self, ) -> float:
        return self.ppt(taxe=self.taxe, unit_price=self.child_price)

    def get_ptt_inf(self) -> float:
        return self.ppt(taxe=self.taxe, unit_price=self.inf_price)

    def get_total_price(self) -> float:
        return (
            self.adult * self.get_ptt_adult()
        ) + (
            self.inf * self.get_ptt_inf()
        ) + (
            self.child * self.get_ptt_inf()
        )
