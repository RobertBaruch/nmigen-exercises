# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from util import main


class Cell3x3(Elaboratable):
    """Logic for the Cell3x3 module."""

    def __init__(self):
        self.input = Signal(9)
        self.output = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the Cell3x3 module."""
        m = Module()

        neighbors = Signal(range(9))
        c = self.input
        m.d.comb += neighbors.eq(c[0] + c[1] + c[2] +
                                 c[3] + c[5] +
                                 c[6] + c[7] + c[8])

        middle = self.input[4]
        m.d.comb += self.output.eq(0)
        with m.If(middle):
            with m.If((neighbors == 2) | (neighbors == 3)):
                m.d.comb += self.output.eq(1)
        with m.Else():
            with m.If(neighbors == 3):
                m.d.comb += self.output.eq(1)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the Cell3x3 module."""
        m = Module()
        m.submodules.c = c = cls()

        s = 0
        for n in range(9):
            if n != 4:
                s += c.input[n]

        with m.If(s == 3):
            m.d.comb += Assert(c.output)
        with m.If(s == 2):
            m.d.comb += Assert(c.output == c.input[4])

        return m, [c.input]


if __name__ == "__main__":
    main(Cell3x3)
