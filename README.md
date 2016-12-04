# contfrac

Python code to explore algebraic numbers written as continued fractions

# Introduction

Just as rational numbers can evaluate to repeating decimals, irrational roots
of quadratic equations evaluate to repeating continued fractions. These
irrational roots of quadratic equations are known as algebraic numbers of
degree 2. In this document we simply call them algebraic numbers.
This repo provides tools for exploring the beautiful world of algebraic numbers
and continued fractions.

# Definitions

We refer to algebraic numbers of degree 2 as simply *algebraic numbers*

Algebraic numbers can be written as **(a + sqrt(r)) / b** where *a* and *b*
are integers, b != 0, and r > 0 and not a perfect square. For example in
(-4 + sqrt(50)) / 7, r = 50, a = -4, b = 7

Since we are studying continued fractions, the algebraic numbers we deal with
from now on are between 0 and 1.

We say an algebraic number **(a + sqrt(r)) / b** is in *normalized* form if *b* divides *r - a^2* and *r*, *a*, and *b* are as small as possible.

For example (-3 + sqrt(31)) / 11 is in normalized form because 11 divides 22,
31 - 3^2. However, (-2 + sqrt(11)) / 5 is not in normalized form because 5
does not divide 7, 11 - 2^2. (-6 + sqrt(124)) / 22 is not in normilised form
either because although 22 divides 88, (-6 + sqrt(124)) / 22 can be reduced to
(-3 + sqrt(31)) / 11 which is in normalized form because 11 divides 22.

Any algebraic number can be written in normalized form by multiplying
its numberator and denominator by some constant.
For example, (-4 + sqrt(44)) / 10 is not in normalized form, but multiplying
the numerator and denominator by 2.5 gives (-10 + sqrt(275)) / 25 which is in
normalized form.

We say that an algebraic number is *strictly repeating* if its continued
fraction has no non repeating pattern preceding the repeating pattern.
For example an algebraic number with continued fraction 3,5,3,5,... is
strictly repeating whereas an algebraic number with continued fraction
1,2,4,3,5,3,5,... is not.

We claim that an algebraic number **(a + sqrt(r)) / b** is strictly repeating
if and only if:

1. b > 0
2. a < 0
3. (a + sqrt(r)) / b < 1
4. (-a + sqrt(r)) / b > 1

For example, (-1 + sqrt(11)) / 4 is strictly repeating because 1 + sqrt(11) > 4
but (-1 + sqrt(11)) / 5 is not because 1 + sqrt(11) < 5.

We say that a strictly repeating algebraic number has *characteristic* of r if
when written in normalized form, the number under the radical is r.
For example, the strictly repeating algebraic number (-3 + sqrt(37)) / 7,
which is already in normalized form, has characteristic of 37.
The strictly repeating algebraic number (-2 + sqrt(11)) / 5 has characteristic
of 275 because (-2 + sqrt(11)) / 5 in normalized form is (-10 + sqrt(275)) / 25.

We say that the set *C(n)* contains all the strictly repeating algebraic
numbers with characteristic n. For each n, the cardinality of C(n) is finite.

We say that the set *P(n)* is a partition of C(n) such that each element
of P(n) contain algebraic numbers whose continued fractions all contain the
same repeating patterns. For instance, the continued fractions
1,2,3,4,1,2,3,4,... and 2,3,4,1,2,3,4,1,... are both strictly repeating and
contain the repeating patterns 1,2,3,4; 2,3,4,1; 3,4,1,2; and 4,1,2,3

# Observations

1. ~~It seems that if n is prime and n mod 4 == 3, then all algebraic numbers
in C(n) have the same repeating sequences in their continued fraction. That
is the cardinality of P(n) is 1.~~ n = 79 is the smallest contridiction to
this conjecture. `len(cont.Partition(79))` is 3

2. It seems that if n is prime and n mod 4 == 1
(the equivalent of n is both prime and can be written as the sum of two squares)
then the elements of P(n) all have odd cardinality.

3. If n is composite and can be written as the sum of two squares then the
elements of P(n) can have even or odd cardinality.

4. It seems that if n cannot be written as the sum of two squares then the
elements of P(n) all have even cardinality.

5. It seems that for any n, the cardinality of the elements of P(n) are either
all even or all odd.


# Getting started

This python repo is for python 2.x. It won't work correctly in python 3.

1. Download the cont.py file
2. Start python by typing python at the mac os X prompt.

Then...

```
>>> import cont
>>> cont.Expand(7, 1, 4)
([1], [10, 3, 2, 3])
```

The continued fraction for (sqrt(7) + 1) / 4 is 1,10,3,2,3,10,3,2,3, ...

# The Python Code

This guide assumes that algebraic numbers are of the form
**(a + sqrt(r)) / b**. Unless explicitly stated, r must be a positive integer
that is not a perfect square, a must be an integer, and b must be an integer
that is not 0.

## cont.AllWith(r)

Returns all algebraic numbers with characteristic r. Returns the empty list
if r is a perfect square.

```
>>> cont.AllWith(31)
[(31, -1, 5), (31, -1, 6), (31, -4, 3), (31, -4, 5), (31, -5, 1), (31, -5, 6), (31, -5, 2), (31, -5, 3)]
```

## cont.Characteristic(r, a, b)

Returns the characteristic of the given algebraic number. Returns 0 if
given algebraic number is not between 0 and 1 or is not strictly repeating.

```
>>> cont.Characteristic(11, -2, 5)
275
```

## cont.Expand(r, a, b)

Returns the continued fraction of the given algebraic number in two parts.
The first part is the non repeating sequence; the second part is the repeating
sequence.

```
>>> cont.Expand(7, -1, 4)
([2], [2, 3, 10, 3])
```

In this exapmple, the continued fraction is 2,2,3,10,3,2,3,10,3, ...

## cont.Normalize(r, a, b)

Returns the given algebraic number in normalized form.

```
>>> cont.Normalize(7, 1, 4)
(28, 2, 8)
```

## cont.Partition(r)

Partitions the algebraic numbers of characteristic *r* according to the
repeating sequence their continued fractions produce. If r is a perfect
square, returns the empty list.

```
>>> for group in cont.Partition(41):
...   print '=' * 35
...   for x in group:
...     print x, cont.Expand(*x)
... 
===================================
(41, -3, 4) ([], [1, 5, 1, 2, 2])
(41, -5, 8) ([], [5, 1, 2, 2, 1])
(41, -5, 2) ([], [1, 2, 2, 1, 5])
(41, -3, 8) ([], [2, 2, 1, 5, 1])
(41, -5, 4) ([], [2, 1, 5, 1, 2])
===================================
(41, -4, 5) ([], [2, 12, 2])
(41, -6, 5) ([], [12, 2, 2])
(41, -6, 1) ([], [2, 2, 12])
```

