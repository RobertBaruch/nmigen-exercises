# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover
from nmigen.lib.coding import PriorityEncoder

from util import main


class UnsignedComparator(Elaboratable):
    """Logic for the UnsignedComparator module."""

    def __init__(self):
        self.a = Signal(16)
        self.b = Signal(16)
        self.lt = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the UnsignedComparator module."""
        m = Module()

        m.d.comb += self.lt.eq(self.a < self.b)

        return m


class SignedComparator(Elaboratable):
    """Logic for the SignedComparator module."""

    def __init__(self):
        self.a = Signal(16)
        self.b = Signal(16)
        self.lt = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the SignedComparator module."""
        m = Module()
        m.submodules.ucmp = ucmp = UnsignedComparator()

        ult = Signal()  # Unsigned less than

        # Hook up the submodule
        m.d.comb += [
            ucmp.a.eq(self.a),
            ucmp.b.eq(self.b),
            ult.eq(ucmp.lt),
        ]

        is_a_neg = self.a[15]
        is_b_neg = self.b[15]

        with m.If(~is_a_neg & ~is_b_neg):
            m.d.comb += self.lt.eq(ult)
        with m.Elif(is_a_neg & ~is_b_neg):
            m.d.comb += self.lt.eq(1)
        with m.Elif(~is_a_neg & is_b_neg):
            m.d.comb += self.lt.eq(0)
        with m.Else():
            m.d.comb += self.lt.eq(ult)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the SignedComparator module."""
        m = Module()
        m.submodules.c = c = cls()

        m.d.comb += Assert(c.lt == (c.a.as_signed() < c.b.as_signed()))

        return m, [c.a, c.b]


if __name__ == "__main__":
    main(SignedComparator)
