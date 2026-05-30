"""Telemetry models."""

from ._base import XtceBaseModel


class TelemetryMetadata(XtceBaseModel):
    """Telemetry related metadata."""

    parameter_types: None
    parameters: None
    containers: None
    messages: None
    streams: None
    algorithms: None
