"""Various utility functions."""

import datetime
from typing import Optional, TypeAlias, TypeVar

from xsdata.models.datatype import (
    DS_MONTH,
    DS_YEAR,
    XmlDateTime,
    XmlDuration,
)

T = TypeVar("T")

XtceValue: TypeAlias = (
    int | float | str | bool | bytes | datetime.timedelta | datetime.datetime
)


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


def coerce(
    value: str,
) -> XtceValue:
    """Coerce an xs string value to a concrete Python type."""
    if isinstance(value, bytes):
        return value

    raw = value.strip()

    try:
        return int(raw, 0)
    except ValueError:
        pass

    try:
        return float(raw)
    except ValueError:
        pass

    lowered = raw.lower()
    if lowered in {"true", "1"}:
        return True
    if lowered in {"false", "0"}:
        return False

    try:
        return bytes.fromhex(raw)
    except ValueError:
        pass

    try:
        return xml_duration_to_timedelta(XmlDuration(raw))
    except ValueError:
        pass

    try:
        return XmlDateTime.from_string(raw).to_datetime()
    except ValueError:
        pass

    return value


def uncoerce(value: XtceValue) -> str:
    """Convert a concrete XTCE value to an xs string value."""
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, datetime.timedelta):
        return str(timedelta_to_xml_duration(value))
    if isinstance(value, datetime.datetime):
        return str(XmlDateTime.from_datetime(value))

    return str(value)


def coerce_optional_int(value: int | str | None) -> int | None:
    """Convert an XTCE integer attribute to a Python int when present."""
    if value is None:
        return None

    if isinstance(value, str):
        return int(value, 0)

    return int(value)


def timedelta_to_xml_duration(td: datetime.timedelta) -> XmlDuration:
    """Convert a timedelta to an XML duration.

    `timedelta` cannot represent years/months, so this only returns `PnDTnHnMnS`.

    """
    negative = td < datetime.timedelta(0)
    absolute = -td if negative else td

    days = absolute.days
    hours, remainder = divmod(absolute.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    seconds_float = seconds + absolute.microseconds / 1_000_000

    duration_str = "-P" if negative else "P"

    if days:
        duration_str += f"{days}D"

    if hours or minutes or seconds_float or not days:
        duration_str += "T"
        if hours:
            duration_str += f"{hours}H"
        if minutes:
            duration_str += f"{minutes}M"

        if seconds_float:
            if absolute.microseconds:
                seconds_str = f"{seconds_float:.6f}".rstrip("0").rstrip(".")
            else:
                seconds_str = str(int(seconds_float))
            duration_str += f"{seconds_str}S"
        elif not hours and not minutes:
            duration_str += "0S"

    return XmlDuration(duration_str)


def xml_duration_to_timedelta(
    duration: XmlDuration,
) -> datetime.timedelta:
    """Convert an XML duration to a timedelta.

    Years and months are always approximated using xsdata's duration constants.

    """
    years = duration.years or 0
    months = duration.months or 0

    days = float(duration.days or 0)
    days += years * (DS_YEAR / 86400)
    days += months * (DS_MONTH / 86400)

    result = datetime.timedelta(
        days=days,
        hours=duration.hours or 0,
        minutes=duration.minutes or 0,
        seconds=duration.seconds or 0,
    )

    return -result if duration.negative else result
