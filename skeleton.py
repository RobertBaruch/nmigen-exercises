# Disable pylint's "your name is too short" warning.
# pylint: disable=C0103
from typing import List, Tuple

from nmigen import Signal, Module, Elaboratable
from nmigen.build import Platform
from nmigen.asserts import Assume, Assert, Cover

from util import main


class MyClass(Elaboratable):
    """Logic for my module.

    This is a skeleton for writing your own modules.
    """

    def __init__(self):
        # Inputs
        self.my_input = Signal()

        # Outputs
        self.my_output = Signal()

    def elaborate(self, _: Platform) -> Module:
        """Implements the logic for my module."""
        m = Module()

        m.d.comb += self.my_output.eq(self.my_input)

        return m

    @classmethod
    def formal(cls) -> Tuple[Module, List[Signal]]:
        """Formal verification for my module."""
        m = Module()
        m.submodules.my_class = my_class = MyClass()

        # Make sure that the output is always the same as the input
        m.d.comb += Assert(my_class.my_input == my_class.my_output)

        # Cover the case where the output is 1.
        m.d.comb += Cover(my_class.my_output == 1)

        return m, [my_class.my_input]


if __name__ == "__main__":
    main(MyClass)
