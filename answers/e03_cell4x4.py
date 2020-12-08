# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from e03_cell3x3 import Cell3x3
from util import main


class Cell4x4(Elaboratable):
    """Logic for the Cell4x4 module."""

    def __init__(self):
        self.input = Signal(16)
        self.output = Signal(4)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the Cell4x4 module."""
        m = Module()

        c = [Cell3x3(), Cell3x3(), Cell3x3(), Cell3x3()]
        m.submodules += c

        # Mapping: inputs:
        #
        #  0  1  2  3
        #  4  5  6  7
        #  8  9 10 11
        # 12 13 14 15
        #
        # outputs:
        #
        #    0  1
        #    2  3

        # Hook up the submodules
        m.d.comb += [
            c[0].input[0].eq(self.input[0]),
            c[0].input[1].eq(self.input[1]),
            c[0].input[2].eq(self.input[2]),
            c[0].input[3].eq(self.input[4]),
            c[0].input[4].eq(self.input[5]),
            c[0].input[5].eq(self.input[6]),
            c[0].input[6].eq(self.input[8]),
            c[0].input[7].eq(self.input[9]),
            c[0].input[8].eq(self.input[10]),
            c[1].input[0:].eq(self.input[1:4]),
            c[1].input[3:].eq(self.input[5:8]),
            c[1].input[6:].eq(self.input[9:12]),
            c[2].input[0:].eq(self.input[4:7]),
            c[2].input[3:].eq(self.input[8:11]),
            c[2].input[6:].eq(self.input[12:15]),
            c[3].input[0:].eq(self.input[5:8]),
            c[3].input[3:].eq(self.input[9:12]),
            c[3].input[6:].eq(self.input[13:]),
        ]

        m.d.comb += [
            self.output[0].eq(c[0].output),
            self.output[1].eq(c[1].output),
            self.output[2].eq(c[2].output),
            self.output[3].eq(c[3].output),
        ]

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the Cell4x4 module."""
        m = Module()
        m.submodules.c = c = cls()

        m.d.comb += Cover(
            (c.output[0] == c.input[5]) &
            (c.output[1] == c.input[6]) &
            (c.output[2] == c.input[9]) &
            (c.output[3] == c.input[10]) &
            (c.output != 0)
        )

        with m.If((c.output == 0b1111) &
                  (c.input[5:7] == 0b11) &
                  (c.input[9:11] == 0b11)):
            m.d.comb += Assert(c.input == 0b0000011001100000)
        return m, [c.input]


if __name__ == "__main__":
    main(Cell4x4)
