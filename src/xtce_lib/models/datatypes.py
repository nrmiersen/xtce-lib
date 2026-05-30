"""Data type models."""

from pydantic import Field

from ._base import XtceBaseModel
from .codec import (
    BinaryDataEncoding,
    FloatDataEncoding,
    IntegerDataEncoding,
    StringDataEncoding,
)
from .common import NameDescriptionBase
from .enums import UnitForm


class Unit(XtceBaseModel):
    """Describe the exponent, factor, form, and description for a unit."""

    # TODO maybe move to a different module
    # TODO maybe add property that builds the unit text

    unit: str = Field(..., examples=["m/s^2", "V", "byte"])
    """The unit text content."""

    factor: str = Field(default="1", examples=["1", "2", "0.5"])
    """Optional attribute used in conjunction with the "power" attribute where some
    programs choose to specify the unit definition with these machine processable
    algebraic features.

    For example, a unit text of "meters" may have a "factor" attribute of 2, resulting
    "2 times meters" as the actual unit. This is not commonly used. The most common
    method for "2 times meters" is to use the str 'unit' attribute in a form like "2*m".
    """

    power: float = Field(default=1.0, examples=[1.0, 2.0, -1.0])
    """Optional attribute used in conjunction with the "factor" attribute where some
    programs choose to specify the unit definition with these machine processable
    algebraic features.

    For example, a unit text of "meters" may have a "power" attribute of 2, resulting
    "meters squared" as the actual unit. This is not commonly used. The most common
    method for "meters squared" is to use the str 'unit' attribute in a form like "m^2".
    """

    form: UnitForm = Field(default=UnitForm.CALIBRATED)
    """The default value "calibrated" is most common practice to specify units at the
    engineering/calibrated value, it is possible to specify an additional Unit element
    for the raw/uncalibrated value.
    """

    description: str | None = Field(
        default=None,
        examples=[
            "meters per second squared is of a property of acceleration.",
            "voltage is of a property of electric potential difference.",
            "represents the length of a buffer in bytes.",
        ],
    )
    """A description of the unit, which may be for expanded human readability or for
    specification of the nature/property of the unit.
    """

class BaseData(NameDescriptionBase):
    """An abstract schema type used by within the schema to derive the other
    simple/primitive engineering form data types.
    """

    units: list[Unit] = Field(default_factory=list)
    """When appropriate, describe the units of measure that are represented by this
    parameter value.
    """

    # TODO validate that there aren't duplicate unit forms

    encoding_type: (
        IntegerDataEncoding
        | FloatDataEncoding
        | StringDataEncoding
        | BinaryDataEncoding
        | None
    ) = Field(...)
    """Optional encoding information for this data type.

    This is only necessary if this data type is telemetered in some form. Local
    variables and derived typically do not require encoding.
    """

    base_type: None
    """Used to derive one Data Type from another - will inherit all the attributes from the baseType any of which may be redefined in this type definition."""

class IntegerData(BaseData):
    pass
