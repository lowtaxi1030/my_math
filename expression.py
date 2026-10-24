from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from variable import Variable

import config
from term import Term


class Expression:
    """整個算式"""

    def __init__(self, *terms: Term):  # , variable: Variable
        self.terms = list(terms)
        self._simplify()

    def copy(self):
        return Expression(*self.terms.copy())

    def __bool__(self):
        return bool(self.terms)

    def evaluate(self):
        return sum(term.evaluate() for term in self.terms)

    """顯示"""

    def __repr__(self):
        return f"Expression(terms={self.terms})"

    def __str__(self):
        resault = []
        for i, term in enumerate(self.terms):
            if i > 0 and term.coefficient > 0:
                resault.append("+")
            resault.append(str(term))
        if not resault:
            return "0"
        return "".join(resault)

    """加減、負號"""

    def __neg__(self):
        return Expression(*(-t for t in self.terms))

    def _add(self, other: int | float | Variable | Term | Expression):
        from term import Term
        from variable import Variable

        if isinstance(other, (int, float)):
            return Expression(*self.terms, Term(0, other))
        elif isinstance(other, Variable):
            return Expression(*self.terms, Term(1, 1, other))
        elif isinstance(other, Term):
            return Expression(*self.terms, other)
        elif isinstance(other, Expression):
            return Expression(*self.terms, *other.terms)

    def __iadd__(self, other: int | float | Variable | Term | Expression):
        self.terms = self._add(other).terms
        return self

    def __add__(self, other: int | float | Variable | Term | Expression):
        return self._add(other)

    def __radd__(self, other: int | float | Variable | Term | Expression):
        return self._add(other)

    def _sub(self, other: int | float | Variable | Term | Expression):
        from term import Term
        from variable import Variable

        if isinstance(other, (int, float)):
            return Expression(*self.terms, -Term(0, other))
        elif isinstance(other, Variable):
            return Expression(*self.terms, -Term(1, 1, other))
        elif isinstance(other, Term):
            return Expression(*self.terms, -other)
        elif isinstance(other, Expression):
            other_expr = -other
            return Expression(*self.terms, *other_expr.terms)

    def __isub__(self, other):
        self.terms = self._sub(other).terms
        return self

    def __sub__(self, other: int | float | Variable | Term | Expression):
        return self._sub(other)

    def __rsub__(self, other: int | float | Variable | Term | Expression):
        from term import Term
        from variable import Variable

        self_expr = -self
        if isinstance(other, (int, float)):
            return Expression(Term(0, other), *self_expr.terms)
        elif isinstance(other, Variable):
            return Expression(Term(1, 1, other), *self_expr.terms)
        elif isinstance(other, Term):
            return Expression(other, *self_expr.terms)
        elif isinstance(other, Expression):
            return Expression(*other.terms, *self_expr.terms)

    """乘除"""

    def _mul(self, other: int | float | Variable | Term | Expression):
        from term import Term
        from variable import Variable

        self_terms = self.terms.copy()

        if isinstance(other, (int, float, Variable, Term)):
            resault_terms = []
            for term in self_terms:
                resault = term * other
                resault_terms.append(resault)

        elif isinstance(other, Expression):
            resault_terms = []

            for term in self_terms:
                for other_term in other.terms:
                    product = term * other_term
                    resault_terms.append(product)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

        return Expression(*resault_terms)

    def __mul__(self, other: int | float | Variable | Term | Expression):
        return self._mul(other)

    def __rmul__(self, other: int | float | Variable | Term | Expression):
        return self._mul(other)

    def __truediv__(self, other: int | float | Variable | Term | Expression):
        from term import Term
        from variable import Variable

        self_terms = self.terms.copy()

        r = Expression(Term(0, 0, None))
        resault_terms = []
        if isinstance(other, (int, float, Variable, Term)):
            for term in self_terms:
                resault = term / other
                resault_terms.append(resault)
        elif isinstance(other, Expression):
            q, r = self._polynomial_long_division(self, other)
            resault_terms = q.terms.copy()
        else:
            raise TypeError(f"Unsupported type for 除法(之後改成英文): {type(other)}")

        return Expression(*resault_terms), r

    def _find_highest_term(self, terms: list[Term]):
        return max(terms, key=lambda term: term.exponent)

    def _polynomial_long_division(self, dividend: Expression, divisor: Expression) -> tuple[Expression, Expression]:
        """dividend: 被除式, divisor: 除式"""

        """
        演算法：
        1.取最高次項相除
        2.用商乘回除式，再相減
        3.重複直到次數降低
        """
        from term import Term

        if not divisor.terms:
            raise ZeroDivisionError("division by zero (divisor.terms)")

        if not dividend.terms:
            return Expression(), Expression()

        final_quotient: Expression = Expression(Term(0, 0, None))
        remainder = dividend.copy()

        while True:
            # [Step1] 取最高次項相除
            #  1.找最高次項
            dividend_highest = self._find_highest_term(remainder.terms)
            divisor_highest = self._find_highest_term(divisor.terms)

            if dividend_highest.exponent < divisor_highest.exponent:
                return Expression(), dividend

            #  2.相除
            quotient = dividend_highest / divisor_highest
            final_quotient += quotient

            # [Step2] 用商乘回除式，再相減
            org_rem_exponent = self._find_highest_term(remainder.terms).exponent
            remainder -= divisor * quotient

            if not remainder.terms:
                break

            new_rem_exponent = self._find_highest_term(remainder.terms).exponent

            if new_rem_exponent >= org_rem_exponent:
                raise config.MathError("remainder's exponent haven't decreased")

            # [Step3] 重複直到次數降低
            if remainder.terms == [] or self._find_highest_term(remainder.terms).exponent < divisor_highest.exponent:
                break

        return final_quotient, remainder

    """同類項合併"""

    def _simplify(self):
        simplified_terms: list[Term] = []

        for term in self.terms:
            found = False
            for i, sim_term in enumerate(simplified_terms):
                same_var = sim_term.name == term.name
                same_exponent = sim_term.exponent == term.exponent
                if same_var and same_exponent:
                    simplified_terms[i].coefficient += term.coefficient
                    found = True
                    break

            if not found:
                simplified_terms.append(term)

        self.terms = [term for term in simplified_terms if term.coefficient != 0]
