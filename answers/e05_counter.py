# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from util import main


class Counter(Elaboratable):
    """Logic for the Counter module."""

    def __init__(self):
        self.count = Signal(4, reset=1)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the Counter module."""
        m = Module()

        with m.If(self.count == 9):
            m.d.sync += self.count.eq(1)
        with m.Else():
            m.d.sync += self.count.eq(self.count+1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the Counter module."""
        m = Module()
        m.submodules.c = c = cls()

        m.d.comb += Assert((c.count >= 1) & (c.count <= 9))
        m.d.comb += Cover(c.count == 3)

        return m, []


if __name__ == "__main__":
    main(Counter)
