# Exercise 4: Signs

## What you'll do, part 1:

Write a module that takes a 64-bit signed number, and negates it in three ways:

* Invert and add 1.
* Directly negate it.
* Starting from the least significant bit, copy up to and including the first 1, then invert the remaining bits.

That last one seems a bit strange, but it works like this (using 8-bit numbers):

Given as input `11101000`, copy up to and including the first 1 (`1000`), then invert the remaining bits: `00011000`. Compare this to inverting first (`00010111`) and adding one: `00011000`. Hey, at least the last technique doesn't require an adder.

Formally verify that:

* These three techniques always result in the same number.
* The most significant bit of the number being set always means it is less than 0.

When you complete this exercise, think about how long the formal verification engine took to run. Formal verification is not a brute-force process. If it were, then even at one check per nanosecond, it would take over 500 years to verify every 64-bit number. Rather, the formal verification engine is a solver, technically an [SMT solver](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories), and every built-in theory such a solver has enables the solver to shortcut some brute-force approaches. The solver we have configured to use in the `[engines]` section of the sby file is the [Z3 solver](https://en.wikipedia.org/wiki/Z3_Theorem_Prover), which has overall good performance.

### Signedness

Up until now, when you've created a Signal, you've created unsigned signals. This means that arithmetic and comparisons on them are unsigned. So, the 4-bit unsigned number `1000` is always *greater* than the 4-bit unsigned number `0111`.

However, in 2's complement, `1000` is -8 while `0111` is 7, which means that if these 4-bit signals were treated as *signed*, `1000` should be *less* than `0111`.

```python
x = Signal(signed(4))
y = Signal(signed(4))
m.d.comb += [
    x.eq(0b1000),
    y.eq(0b0111),
    Assert(x < y),
]
```

To treat an unsigned (or signed) signal as signed:

```python
x = Signal(4)
y = Signal(4)
m.d.comb += [
    x.eq(0b1000),
    y.eq(0b0111),
    Assert(x.as_signed() < y.as_signed()),
]
```

There is also a corresponding `as_unsigned()` function to convert a signed (or unsigned) signal to an unsigned signal.

Negating a signal always results in a signed signal, regardless of whether the input signal is signed or unsigned:

```python
x = Signal(4)
y = Signal(4)
m.d.comb += [
    x.eq(0b0011),
    y.eq(0b1101),
    Assert(y > x),
    Assert(-x < x),
]
```

Equality, on the other hand, does not take into account signedness. It is bit-for-bit equality:

```python
x = Signal(4)
y = Signal(4)
m.d.comb += [
    x.eq(0b0011),
    y.eq(0b1101),
    Assert(y > x),
    Assert(-x == y),
]
```

All arithmetic operations that apply to signed signals are signed. For example, right shifts do take into account signedness, and the result is the same signedness as the input:

```python
x = Signal(4)
y = Signal(signed(4))
m.d.comb += [
    x.eq(0b1000),
    y.eq(0b1000),
    Assert((x >> 1) == 0b0100),
    Assert((y >> 1) == 0b1100),
]
```

### Library: priority encoder

A *priority encoder* is a circuit that takes an N-bit input and outputs the position of the first set bit, where "first" could mean most significant or least significant. nMigen has a coding library with a PriorityEncoder module built in, which outputs the position of the first least significant bit set.

```python
from nmigen.lib.coding import PriorityEncoder

enc = PriorityEncoder(width=8)
input = Signal(8)
output = Signal(3)
bit_set = Signal()

m.d.comb += [
    enc.i.eq(input),
    output.eq(enc.o),
    bit_set.eq(~enc.n),  # n really means that the input is zero
]
```

For example, the input `0101000` will result in the output being 3 and bit_set being high.

### Limitations on slices

Slices such as `x[1:4]` require integers as indices, not signals. So you can't have:

```python
x = Signal(8)
y = Signal(3)
z = x[y]  # Results in an error
```

You can achieve the same effect using bit tricks. For example, `1 << y` gives you a 1 in the yth bit position. `(x >> y) & 1` gives you the yth bit of x.

What does `(-1 << y) & x` give you?

-----

Interested in more bit-manipulation tricks? Check out Knuth's The Art of Computer Programming, Volume 4A, chapter 7.1.3 (Bitwise Tricks and Techniques). Hacker's Delight also contains copious bit manipulation fun.

-----

## What you'll do, part 2:

Suppose you have a chip that can compare two 16-bit numbers, but only as unsigned numbers. It outputs whether the first is less than the second. Write such a module.

Now write another module that uses the above module, and based only the most significant bits (i.e. the sign bits) of the original inputs, and the output of the unsigned comparator, outputs whether the first is less than the second, treated as *signed* numbers. The idea here is that you're limited to an unsigned comparator, and need a signed comparator.

Formally verify that the output of your module is correct, by using `as_signed()`.

## Stumped?

The answers are in [`answers/e04_negate.py`](answers/e04_negate.py) and [`answers/e04_signed_compare.py`](answers/e04_signed_compare.py)
