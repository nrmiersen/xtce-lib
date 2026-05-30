"""Argument models."""

from ._base import XtceBaseModel


class StringArgument(XtceBaseModel):
    pass


class EnumeratedArgument(XtceBaseModel):
    pass


class IntegerArgument(XtceBaseModel):
    pass


class BinaryArgument(XtceBaseModel):
    pass


class FloatArgument(XtceBaseModel):
    pass


class BooleanArgument(XtceBaseModel):
    pass


class RelativeTimeArgument(XtceBaseModel):
    pass


class AbsoluteTimeArgument(XtceBaseModel):
    pass


class ArrayArgument(XtceBaseModel):
    pass


class AggregateArgument(XtceBaseModel):
    pass
