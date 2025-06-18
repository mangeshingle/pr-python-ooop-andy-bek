from dataclasses import dataclass, field
from functools import total_ordering
from typing import List


@dataclass(frozen=True)
class Stock:
    ticker: str
    price: float
    divident: float = field(default=0.0)
    divident_frequency: int = field(default=4)

    @property
    def annual_divident(self):
        return self.divident * self.divident_frequency


@total_ordering
@dataclass
class Position:
    stock: Stock
    shares: int

    def __eq__(self, other):
        if type(self) is not type(other):
            raise TypeError("Cannot compare different types")
        return self.stock.price * self.shares == other.stock.price * other.shares

    def __lt__(self, other):
        if type(self) is not type(other):
            raise TypeError("Cannot compare different types")
        return self.stock.price * self.shares < other.stock.price * other.shares


@dataclass
class Portfolio:
    holdings: List[Position]

    @property
    def value(self):
        return sum(
            [position.shares * position.stock.price for position in self.holdings]
        )

    @property
    def portfolio_yield(self):
        return (
            sum(
                [
                    position.shares * position.stock.annual_divident
                    for position in self.holdings
                ]
            )
            / self.value
        )
