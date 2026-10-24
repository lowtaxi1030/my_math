
DISPLAY_EXPONENT_NUMS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


def to_superscript(exponent: int) -> str:
    return "".join(DISPLAY_EXPONENT_NUMS[digit] for digit in str(exponent))


def same_variable_cheak(self_name, other_name):
    return self_name is not None and other_name is not None and self_name != other_name


class MathError(Exception): ...

