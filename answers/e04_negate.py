# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover
from nmigen.lib.coding import PriorityEncoder

from util import main


class Negate(Elaboratable):
    """Logic for the Negate module."""

    def __init__(self):
        self.input = Signal(64)
        self.output1 = Signal(64)  # invert and add 1
        self.output2 = Signal(64)  # direct negation
        self.output3 = Signal(64)  # using priority encoder

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the Negate module."""
        m = Module()
        m.submodules.enc = enc = PriorityEncoder(64)

        m.d.comb += self.output1.eq(~self.input + 1)
        m.d.comb += self.output2.eq(-self.input)
        m.d.comb += enc.i.eq(self.input)

        with m.If(enc.n):
            m.d.comb += self.output3.eq(0)
        with m.Else():
            neg1 = Signal(64)
            m.d.comb += neg1.eq(-1)
            #          n
            # 1111111111000000  # mask = -1 << n
            # 0000000000111111  # lower_mask = ~(-1 << n)
            # 0000000001000000  # 1 << n
            mask = Signal(64)
            m.d.comb += mask.eq(neg1 << enc.o)
            lower_mask = ~mask
            m.d.comb += self.output3.eq((~self.input & mask)
                                        | (self.input & lower_mask)
                                        | (1 << enc.o))

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the Negate module."""
        m = Module()
        m.submodules.c = c = cls()

        m.d.comb += Assert(c.output1 == c.output2)
        m.d.comb += Assert(c.output2 == c.output3)
        m.d.comb += Assert(c.output1[63] == (c.output1.as_signed() < 0))

        return m, [c.input]


if __name__ == "__main__":
    main(Negate)
