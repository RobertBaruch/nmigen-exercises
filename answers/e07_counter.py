# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable, ClockSignal, ResetSignal, ClockDomain
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover, Past, Initial, Rose

from util import main


class Counter(Elaboratable):
    """Logic for the Counter module."""

    def __init__(self):
        self.count = Signal(40, reset=1)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the Counter module."""
        m = Module()

        with m.If(self.count == 999_999_999_999):
            m.d.sync += self.count.eq(1)
        with m.Else():
            m.d.sync += self.count.eq(self.count+1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the Counter module."""
        m = Module()
        m.submodules.c = c = cls()

        m.d.comb += Assert((c.count >= 1) & (c.count <= 999_999_999_999))

        sync_clk = ClockSignal("sync")
        sync_rst = ResetSignal("sync")

        with m.If(Rose(sync_clk) & ~Initial()):
            with m.If(c.count == 1):
                m.d.comb += Assert(Past(c.count) == 999_999_999_999)
            with m.Else():
                m.d.comb += Assert(c.count == (Past(c.count) + 1))

        # Make sure the clock is clocking
        m.d.comb += Assume(sync_clk == ~Past(sync_clk))

        # Don't want to test what happens when we reset.
        m.d.comb += Assume(~sync_rst)

        return m, [sync_clk, sync_rst]


if __name__ == "__main__":
    main(Counter)
