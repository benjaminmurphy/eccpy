#!/usr/bin/env python3

class Curve:
    """A class representing an elliptic curve."""

    class Integer:
        """A class representing an integer with a given modulus."""
        def __init__(self, modulus: int, value: int) -> None:
            self.modulus = modulus
            self.value = value % self.modulus

        def __add__(self, other: "Integer") -> "Integer":
            if other.modulus != self.modulus:
                raise Exception("Cannot add values with different moduli.")
            return Curve.Integer(self.modulus, self.value + other.value)

        def __sub__(self, other: "Integer") -> "Integer":
            if other.modulus != self.modulus:
                raise Exception("Cannot subtract values with different moduli.")
            return Curve.Integer(self.modulus, self.value - other.value)

        def __mul__(self, other: "Integer") -> "Integer":
            if other.modulus != self.modulus:
                raise Exception("Cannot multiply values with different moduli.")
            return Curve.Integer(self.modulus, self.value * other.value)

        def __truediv__(self, other: "Integer") -> "Integer":
            if other.value == 0:
                raise Exception("Cannot divide by zero.")
            return self * other.inverse()

        def inverse(self) -> "Integer":
            for n in range(1, self.modulus):
                if n * self.value % self.modulus == 1:
                    return Curve.Integer(self.modulus, n)
            raise Exception("%s: No inverse modulo %s" % (
                self.value,
                self.modulus,
            ))

        def __pow__(self, n: int) -> "Integer":
            return Curve.Integer(self.modulus, self.value ** n)

        def __eq__(self, other: "Integer") -> bool:
            return self.value == other.value and self.modulus == other.modulus

        def __str__(self) -> str:
            return str(self.value)

    class Point:
        """A class representing a point on the given elliptic curve."""
        def __init__(self, curve: "Curve", X: "Integer", Y: "Integer") -> None:
            self.curve = curve
            self.X = X
            self.Y = Y

            if self.Y ** 2 != (self.X ** 3) + (curve.A * self.X) + (curve.B):
                raise Exception("(%s, %s): Not a point on curve." % (self.X, self.Y))

        def __eq__(self, other: "Point") -> bool:
            return self.X == other.X and self.Y == other.Y

        def __add__(self, other: "Point") -> "Point":
            if self == other:
                m = (Curve.Integer(self.curve.N, 3) * (self.X ** 2) + self.curve.A) * (Curve.Integer(self.curve.N, 2) * self.Y).inverse()
            else:
                m = (self.Y - other.Y) / (self.X - other.X)

            new_x = (m ** 2) - self.X - other.X
            new_y = m * (self.X - new_x) - self.Y

            return Curve.Point(self.curve, new_x, new_y)

        def __neg__(self) -> "Point":
            return Curve.Point(self.curve, self.Y * Curve.Integer(self.curve.N, -1))

        def copy(self) -> "Point":
            return Curve.Point(self.curve, self.X, self.Y)

        def times(self, n: int) -> "Point":
            result = self.copy()
            for _ in range(n-1):
                result += self

            return result

        def __str__(self) -> str:
            return "(%s, %s)" % (self.X, self.Y)

    def __init__(self, N: int, A: int, B: int) -> None:
        self.N = N
        self.A = Curve.Integer(N, A)
        self.B = Curve.Integer(N, B)

    def point(self, X: int, Y: int) -> Point:
        return Curve.Point(
            self,
            Curve.Integer(self.N, X),
            Curve.Integer(self.N, Y),
        )
