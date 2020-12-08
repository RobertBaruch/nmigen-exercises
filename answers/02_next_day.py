# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from util import main


class NextDay(Elaboratable):
    """Logic for the NextDay module."""

    def __init__(self):
        # Inputs
        self.year = Signal(range(1, 10000))
        self.month = Signal(range(1, 13))
        self.day = Signal(range(1, 32))

        # Outputs
        self.next_year = Signal(range(1, 10001))
        self.next_month = Signal.like(self.month)
        self.next_day = Signal.like(self.day)
        self.invalid = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the NextDay module."""
        m = Module()

        is_leap_year = Signal()
        max_day = Signal.like(self.day)

        m.d.comb += is_leap_year.eq(0)  # We can override this below!
        with m.If((self.year % 4) == 0):
            m.d.comb += is_leap_year.eq(1)
            with m.If((self.year % 100) == 0):
                m.d.comb += is_leap_year.eq(0)
                with m.If((self.year % 400) == 0):
                    m.d.comb += is_leap_year.eq(1)

        with m.Switch(self.month):
            with m.Case(1, 3, 5, 7, 8, 10, 12):
                m.d.comb += max_day.eq(31)
            with m.Case(2):
                m.d.comb += max_day.eq(28 + is_leap_year)
            with m.Default():
                m.d.comb += max_day.eq(30)

        m.d.comb += self.next_year.eq(self.year)
        m.d.comb += self.next_month.eq(self.month)
        m.d.comb += self.next_day.eq(self.day + 1)

        with m.If(self.day == max_day):
            m.d.comb += self.next_day.eq(1)
            m.d.comb += self.next_month.eq(self.month + 1)
            with m.If(self.month == 12):
                m.d.comb += self.next_month.eq(1)
                m.d.comb += self.next_year.eq(self.year + 1)

        m.d.comb += self.invalid.eq(0)
        with m.If((self.day < 1) | (self.day > max_day) |
                  (self.month < 1) | (self.month > 12) |
                  (self.year < 1) | (self.year > 9999)):
            m.d.comb += self.invalid.eq(1)

        with m.If(self.invalid):
            m.d.comb += self.next_year.eq(0)
            m.d.comb += self.next_month.eq(0)
            m.d.comb += self.next_day.eq(0)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the NextDay module."""
        m = Module()
        m.submodules.nd = nd = NextDay()

        # We don't have to create a signal here. Using is_zero is like just copying the logic.
        is_zero = ((nd.next_year == 0) &
                   (nd.next_month == 0) &
                   (nd.next_day == 0))
        m.d.comb += Assert(nd.invalid == is_zero)

        all_nonzero = ((nd.next_year != 0) &
                       (nd.next_month != 0) &
                       (nd.next_day != 0))
        m.d.comb += Assert(all_nonzero | is_zero)

        with m.If(~nd.invalid):
            with m.If(nd.day == 31):
                m.d.comb += Assert(nd.next_day == 1)
            with m.If((nd.month == 12) & (nd.day == 31)):
                m.d.comb += Assert(nd.next_month == 1)

        with m.If(((nd.year % 2) == 1) & (nd.month == 2) & (nd.day == 29)):
            m.d.comb += Assert(nd.invalid)

        m.d.comb += Cover((nd.next_month == 2) & (nd.next_day == 29))

        return m, [nd.year, nd.month, nd.day]


if __name__ == "__main__":
    main(NextDay)
