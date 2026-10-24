from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from expression import Expression
    from term import Term
    from variable import Variable

# import config
import math
from fractions import Fraction as PyFraction


class Fraction:

    @staticmethod
    def _convert_float(number: int | float):
        resault = PyFraction(str(number))
        return resault.numerator, resault.denominator

    def _init_num(self, num: int | float | Variable | Term | Expression):
        from expression import Expression
        from term import Term
        from variable import Variable

        if isinstance(num, (int, float)):
            resault = num
        elif isinstance(num, Variable):
            resault = Expression(Term(1, 1, num))
        elif isinstance(num, Term):
            resault = Expression(num)
        elif isinstance(num, Expression):
            resault = num.copy()
        else:
            raise TypeError(f"wrong type: {type(num)}")

        return resault

    def __init__(
        self,
        numerator: int | float | Variable | Term | Expression,
        denominator: int | float | Variable | Term | Expression,
    ):
        """
        numerator: 分子
        denominator: 分母
        """
        self.numerator = self._init_num(numerator)
        self.denominator = self._init_num(denominator)
        self._cheak_denominator_zero()

        self._simplify()

    def _cheak_denominator_zero(self):
        if not self.denominator:  # 空列表、0
            raise ZeroDivisionError("denominator can't be zero")

    def _handle_div(self, target: int | float | Expression):
        from expression import Expression

        if isinstance(target, (int, float)):
            return target
        elif isinstance(target, Expression):
            return target.evaluate()
        else:
            raise TypeError(f"wrong target type: {type(target)}")

    def evaluate(self):
        if (res := self._handle_div(self.denominator)) == 0:
            raise ZeroDivisionError("division by zero")
        return self._handle_div(self.numerator) / res

    """顯示"""

    def __repr__(self):
        return f"Fraction(numerator={self.numerator!r}, denominator={self.denominator!r})"

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        n = str(self.numerator)
        d = str(self.denominator)
        width = max(len(n), len(d))
        return "\n".join((n.rjust(width), "—" * width, d.rjust(width)))

    """加減"""

    def _add(self, other: int | float | Fraction):
        if isinstance(other, (int, float)):
            new_numerator = self.numerator + self.denominator * other
            new_denominator = self.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator + self.denominator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        else:
            raise TypeError("")

    def __add__(self, other: int | float | Fraction):
        return self._add(other)

    def __radd__(self, other: int | float | Fraction):
        return self._add(other)

    def __sub__(self, other: int | float | Fraction):
        if isinstance(other, (int, float)):
            new_numerator = self.numerator - self.denominator * other
            new_denominator = self.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, Fraction):
            new_numerator = self.numerator * other.denominator - self.denominator * other.numerator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        else:
            raise TypeError("")

    def __rsub__(self, other: int | float | Fraction):
        if isinstance(other, (int, float)):
            new_numerator = self.denominator * other - self.numerator
            new_denominator = self.denominator
            return Fraction(new_numerator, new_denominator)
        elif isinstance(other, Fraction):
            new_numerator = self.denominator * other.numerator - self.numerator * other.denominator
            new_denominator = self.denominator * other.denominator
            return Fraction(new_numerator, new_denominator)
        else:
            raise TypeError("")

    """乘除"""

    def _mul(self, other: int | float | Variable | Term | Expression | Fraction):
        from expression import Expression
        from term import Term
        from variable import Variable

        if isinstance(other, (int, float)):
            return Fraction(self.numerator * other, self.denominator)
        elif isinstance(other, (Variable, Term, Expression)):
            other_f = Fraction(other, 1)
        elif isinstance(other, Fraction):
            return Fraction(
                self.numerator * other.numerator,
                self.denominator * other.denominator,
            )
        else:
            raise TypeError("")

        return self._mul(other_f)

    def __mul__(self, other: int | float | Variable | Term | Expression | Fraction):
        return self._mul(other)

    def __rmul__(self, other: int | float | Variable | Term | Expression | Fraction):
        return self._mul(other)

    def __truediv__(self, other: int | float | Variable | Term | Expression | Fraction):
        from expression import Expression
        from term import Term
        from variable import Variable

        if isinstance(other, (int, float)):
            return Fraction(self.numerator, self.denominator * other)
        elif isinstance(other, (Variable, Term, Expression)):
            other_f = Fraction(other, 1)
        elif isinstance(other, Fraction):
            return Fraction(
                self.numerator * other.denominator,
                self.denominator * other.numerator,
            )
        else:
            raise TypeError("")

        return self.__truediv__(other_f)

    def __rtruediv__(self, other: int | float | Variable | Term | Expression | Fraction):
        from expression import Expression
        from term import Term
        from variable import Variable

        if isinstance(other, (int, float)):
            return Fraction(self.denominator * other, self.numerator)
        elif isinstance(other, (Variable, Term, Expression)):
            other_f = Fraction(other, 1)
        elif isinstance(other, Fraction):
            return Fraction(
                self.denominator * other.numerator,
                self.numerator * other.denominator,
            )
        else:
            raise TypeError("")

        return self.__rtruediv__(other_f)

    """約分"""

    def _simplify(self):
        self._cheak_denominator_zero()
        if isinstance(self.numerator, (int, float)) and isinstance(self.denominator, (int, float)):
            if isinstance(self.numerator, int) and isinstance(self.denominator, int):
                self.numerator, self.denominator = self._normalize_fraction(self.numerator, self.denominator)
            if isinstance(self.numerator, float) or isinstance(self.denominator, float):
                n1, d1 = self._convert_float(self.numerator)
                n2, d2 = self._convert_float(self.denominator)
                new_n = n1 * d2
                new_d = n2 * d1
                self.numerator, self.denominator = self._normalize_fraction(new_n, new_d)

    @staticmethod
    def _normalize_fraction(n: int, d: int) -> tuple[int, int]:
        s = math.gcd(abs(n), abs(d))
        n //= s
        d //= s
        if (n < 0) != (d < 0):
            n = -abs(n)
            d = abs(d)
        else:
            n = abs(n)
            d = abs(d)
        return n, d
