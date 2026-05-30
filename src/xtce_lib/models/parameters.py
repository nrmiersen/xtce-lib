"""Parameter models."""

from ._base import XtceBaseModel


class StringParameter(XtceBaseModel):
    pass


class EnumeratedParameter(XtceBaseModel):
    pass


class IntegerParameter(XtceBaseModel):
    pass


class BinaryParameter(XtceBaseModel):
    pass


class FloatParameter(XtceBaseModel):
    pass


class BooleanParameter(XtceBaseModel):
    pass


class RelativeTimeParameter(XtceBaseModel):
    pass


class AbsoluteTimeParameter(XtceBaseModel):
    pass


class ArrayParameter(XtceBaseModel):
    pass


class AggregateParameter(XtceBaseModel):
    pass


class Parameter(XtceBaseModel):
    pass


class ParameterRef(XtceBaseModel):
    pass
