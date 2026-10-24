from __future__ import annotations

import config
from expression import Expression
from fraction import Fraction
from term import Term


class Variable:
    def __init__(self, name: str):
        self.name = name
        self.value = None

    def __repr__(self):
        return f"Variable(name={self.name}, value={self.value})"

    def set(self, number: int | float):
        self.value = number

    def clear(self):
        self.value = None

    def evaluate(self):
        if self.value is None:
            raise config.MathError("this Variable has no value")
        return self.value

    """加減"""

    def __neg__(self):
        return Expression(
            Term(
                exponent=1,
                coefficient=-1,
                variable=self,
            )
        )

    def _add_and_sub(self, other: int | float | Term | Expression | Variable, sign: int):
        """sign: 只能是1、-1"""

        if sign not in [1, -1]:
            raise ValueError("sign only can be 1 or -1")

        self_term = Term(exponent=1, coefficient=1, variable=self)
        if isinstance(other, (int, float)):
            return Expression(self_term, Term(exponent=0, coefficient=other if sign == 1 else -other))
        elif isinstance(other, Term):
            return Expression(self_term, other if sign == 1 else -other)
        elif isinstance(other, Expression):
            return Expression(self_term, *(other if sign == 1 else -other).terms)
        elif isinstance(other, Variable):
            return Expression(self_term, Term(exponent=1, coefficient=sign, variable=other))
        else:
            raise TypeError("Unsupported type for " + ("addition" if sign == 1 else "subtraction") + f": {type(other)}")

    def _add(self, other: int | float | Term | Expression | Variable):
        return self._add_and_sub(other, 1)

    def __add__(self, other):
        return self._add(other)

    def __radd__(self, other):
        return self._add(other)

    def __sub__(self, other):
        return self._add_and_sub(other, -1)

    def __rsub__(self, other: int | float | Term | Expression | Variable):
        self_term = Term(exponent=1, coefficient=-1, variable=self)
        if isinstance(other, (int, float)):
            return Expression(Term(exponent=0, coefficient=other), self_term)
        elif isinstance(other, Term):
            return Expression(Term(exponent=other.exponent, coefficient=other.coefficient, variable=other.variable), self_term)
        elif isinstance(other, Expression):
            return Expression(
                *[Term(exponent=term.exponent, coefficient=term.coefficient, variable=term.variable) for term in other.terms], self_term
            )
        elif isinstance(other, Variable):
            return Expression(Term(exponent=1, coefficient=1, variable=other), self_term)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")

    """乘除"""

    def _mul(self, other: int | float | Term | Expression | Variable):
        self_term = Term(1, 1, self)
        if isinstance(other, (int, float)):
            return Expression(Term(1, other, self))
        elif isinstance(other, Variable):
            if other.name != self.name:
                raise ValueError("Only variables of the same type are supported")
            other_term = Term(1, 1, other)
            return Expression(self_term * other_term)
        elif isinstance(other, Term):
            return Expression(self_term * other)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __mul__(self, other):
        return self._mul(other)

    def __rmul__(self, other):
        return self._mul(other)

    def __truediv__(self, other: int | float | Term | Variable):
        self_term = Term(exponent=1, coefficient=1, variable=self)
        if isinstance(other, (int, float)):
            self_term.coefficient = 1 / other
            return Expression(self_term)
        elif isinstance(other, Term):
            return Expression(self_term / other)
        elif isinstance(other, Variable):
            if other.name != self.name:
                raise ValueError("Only variables of the same type are supported")
            other_term = Term(1, 1, other)
            return Expression(self_term / other_term)
        else:
            raise TypeError(f"Unsupported type for 除法(之後改成英文): {type(other)}")

    def __rtruediv__(self, other):
        return Fraction(other, self)

    """次方"""

    def __pow__(self, other: int) -> int | Expression:
        if isinstance(other, int):
            if other < 0:
                return Fraction(1, Expression(Term(abs(other), 1, self)))
            if other == 0:
                return 1
            return Expression(Term(other, 1, self))
        raise TypeError("exponent must be an integer")
