"""Time models."""

import datetime

from pydantic import Field

from xtce_lib.models._base import XtceBaseModel

from .enum import EpochTime, TimeUnits
from .reference import ParameterInstanceRef


class TimeAssociation(ParameterInstanceRef):
    interpolate_time: bool = Field(default=True)
    offset: float | None = Field(default=None)
    unit: TimeUnits = Field(default=TimeUnits.SECONDS)


class ReferenceTime(XtceBaseModel):
    # TODO maybe give separate attributes for offset or epoch
    reference_type: (
        ParameterInstanceRef | datetime.date | datetime.datetime | EpochTime | None
    ) = Field(default=None)  # TODO XmlDate, XmlDateTime
