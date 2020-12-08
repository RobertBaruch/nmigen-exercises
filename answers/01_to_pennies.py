# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from util import main


class ToPennies(Elaboratable):
    """Logic for the ToPennies module."""

    def __init__(self):
        # Inputs
        self.pennies = Signal(8)
        self.nickels = Signal(4)
        self.dimes = Signal(4)
        self.quarters = Signal(4)
        self.dollars = Signal(4)

        # Outputs
        # The maximum is 2355 pennies, so we'll need 12 bits
        self.pennies_out = Signal(12)

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for the ToPennies module."""
        m = Module()

        m.d.comb += self.pennies_out.eq(self.pennies +
                                        5 * self.nickels +
                                        10 * self.dimes +
                                        25 * self.quarters +
                                        100 * self.dollars)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for the ToPennies module."""
        m = Module()
        m.submodules.to_pennies = to_pennies = ToPennies()

        m.d.comb += Cover((to_pennies.pennies == 37) &
                          (to_pennies.nickels == 3) &
                          (to_pennies.dimes == 10) &
                          (to_pennies.quarters == 5) &
                          (to_pennies.dollars == 2))

        m.d.comb += Cover(to_pennies.pennies_out == 548)

        m.d.comb += Cover((to_pennies.pennies_out == 64) &
                          (to_pennies.nickels == 2 * to_pennies.dimes) &
                          (to_pennies.dimes > 0))

        m.d.comb += Assert((to_pennies.pennies_out % 5)
                           == (to_pennies.pennies % 5))

        with m.If(to_pennies.pennies == 0):
            m.d.comb += Assert((to_pennies.pennies % 5) == 0)

        return m, [to_pennies.pennies, to_pennies.nickels, to_pennies.dimes,
                   to_pennies.quarters, to_pennies.dollars]


if __name__ == "__main__":
    main(ToPennies)
