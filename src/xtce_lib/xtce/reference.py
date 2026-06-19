"""Reference models."""

from pydantic import Field

from ._base import XtceBaseModel


class ParameterRef(XtceBaseModel):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class ParameterInstanceRef(ParameterRef):
    instance: int = Field(default=0)
    use_calibrated_value: bool = Field(default=True)


class ContainerRef(XtceBaseModel):
    container_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class ServiceRef(XtceBaseModel):
    service_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class StreamRef(XtceBaseModel):
    stream_ref: str = Field(
        ..., pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+"
    )


class InputParameterInstanceRef(ParameterInstanceRef):
    input_name: str | None = Field(default=None)


class OutputParameterRef(ParameterRef):
    output_name: str | None = Field(default=None)


class ArgumentInstanceRef(XtceBaseModel):
    argument_ref: str = Field(
        ..., pattern=r"([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)"
    )
    use_calibrated_value: bool = Field(default=True)
