"""Trigger models."""

from pydantic import Field

from ._base import XtceBaseModel


class BaseTrigger(XtceBaseModel):
    # Nothing
    pass


class OnParameterUpdateTrigger(BaseTrigger):
    parameter_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+([^\.\[\]:/ \t]+(\[[0-9]+\])*(\.[^\.\[\]:/ \t]+(\[[0-9]+\])*)*)*",
    )


class OnContainerUpdateTrigger(BaseTrigger):
    container_ref: str = Field(
        ...,
        pattern=r"(/?(|\.{1,2}/|[^.\[\]:/ \t]+))*[^.\[\]:/ \t]+",
    )


class OnPeriodicRateTrigger(BaseTrigger):
    fire_rate_in_seconds: float = Field(...)  # GE 0?


class TriggerSet(XtceBaseModel):
    triggers: list[
        OnParameterUpdateTrigger | OnContainerUpdateTrigger | OnPeriodicRateTrigger
    ] = Field(default_factory=list)
    name: str | None = Field(default=None)
    trigger_rate: int = Field(default=1, ge=0)
