from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from variable import Variable

import config


class Term:
    """單一項"""

    def __init__(self, exponent: int, coefficient: float, variable: Variable | None = None):
        """
        exponent: 指數
        coefficient: 係數
        variable: 變數
        """

        if exponent < 0:
            raise ValueError("exponent must greater then 0")
        self.exponent = 0 if variable is None else exponent
        self.coefficient = coefficient
        self.variable = variable if self.exponent != 0 else None

    @property
    def name(self):
        if self.variable is None:
            return None
        return self.variable.name

    def evaluate(self) -> int | float:
        if self.variable is None:
            return self.coefficient
        return self.variable.evaluate() ** self.exponent * self.coefficient

    """顯示"""

    def __repr__(self):
        return f"Term(exponent={self.exponent}, coefficient={self.coefficient}, variable={self.variable})"

    def __str__(self) -> str:
        if self.coefficient == -1:
            display_coeff = "-" if self.variable is not None else "-1"
        elif self.coefficient == 1:
            display_coeff = "" if self.variable is not None else "1"
        else:
            display_coeff = str(self.coefficient)
        display_expo = "" if self.exponent <= 1 else config.to_superscript(self.exponent)
        display_vari = "" if self.name is None else self.variable.name
        return display_coeff + display_vari + display_expo

    """"""

    def __neg__(self):
        return Term(
            coefficient=-self.coefficient,
            variable=self.variable,
            exponent=self.exponent,
        )

    def _mul(self, other: int | float | Variable | Term):
        from variable import Variable

        if isinstance(other, (int, float)):
            return Term(
                exponent=self.exponent,
                coefficient=self.coefficient * other,
                variable=self.variable,
            )

        elif isinstance(other, Variable):
            if config.same_variable_cheak(self.name, other.name):
                raise ValueError("Only variables of the same type are supported")

            return Term(
                exponent=self.exponent + 1,
                coefficient=self.coefficient,
                variable=self.variable or other,
            )

        elif isinstance(other, Term):
            if config.same_variable_cheak(self.name, other.name):
                raise ValueError("Only variables of the same type are supported")

            return Term(
                exponent=self.exponent + other.exponent,
                coefficient=self.coefficient * other.coefficient,
                variable=self.variable or other.variable,
            )

        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __mul__(self, other):
        return self._mul(other)

    def __rmul__(self, other):
        return self._mul(other)

    def __truediv__(self, other: int | float | Variable | Term):
        from variable import Variable

        if isinstance(other, (int, float)):
            return Term(
                exponent=self.exponent,
                coefficient=self.coefficient / other,
                variable=self.variable,
            )
        elif isinstance(other, Variable):
            if config.same_variable_cheak(self.name, other.name):
                raise ValueError("Only variables of the same type are supported")

            return Term(
                exponent=self.exponent - 1,
                coefficient=self.coefficient,
                variable=self.variable or other,
            )
        elif isinstance(other, Term):
            if config.same_variable_cheak(self.name, other.name):
                raise ValueError("Only variables of the same type are supported")

            return Term(
                exponent=self.exponent - other.exponent,
                coefficient=self.coefficient / other.coefficient,
                variable=self.variable or other,
            )

        else:
            raise TypeError(f"Unsupported type for 除法(之後改成英文): {type(other)}")
