"""Various utility functions."""

from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(value: Optional[T]) -> T:
    """Return the value if it is not None, otherwise raises a ValueError.

    This is for fields that are defined as Optional in the xsdata bindings but are
    strictly required by the XTCE XSD. Because XSD validation is performed prior to any
    XTCE parsing, it is effectively impossible for these fields to be None at runtime,
    so this function allows us to treat them as non-optional in the code while still
    satisfying the type checker.

    """
    if value is None:
        raise ValueError("nnexpected None for required XTCE field")

    return value


def coerce_optional_int(value: int | str | None) -> int | None:
    """Convert an XTCE integer attribute to a Python int when present."""
    if value is None:
        return None

    if isinstance(value, str):
        return int(value, 0)

    return int(value)
