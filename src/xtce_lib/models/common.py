"""Common base classes."""

from pydantic import Field

from ._base import XtceBaseModel


class Alias(XtceBaseModel):
    """Used to contain an alternate name or ID for the object.

    For example, a parameter may have a mnemonic, an on-board id, and special IDs used
    by various ground software applications; all of these are aliases. Some ground
    system processing equipment has some severe naming restrictions on parameters (e.g.,
    names must less then 12 characters, single case or integral id's only); their
    aliases provide a means of capturing each name in a "nameSpace". Note: the name is
    not reference-able (it cannot be used in a name reference substituting for the name
    of the item of interest).
    """

    name_space: str = Field(
        ...,
        description=(
            'Aliases should be grouped together in a "namespace" so that they can be '
            "switched in and out of data extractions. The namespace generally "
            "identifies the purpose of the alternate name, whether for software "
            "variable names, additional operator names, or whatever the purpose."
        ),
        examples=["Bus", "Payload", "Ground"],
    )
    """Aliases should be grouped together in a "namespace" so that they can be switched
    in and out of data extractions.

    The namespace generally identifies the purpose of the alternate name, whether for
    software variable names, additional operator names, or whatever the purpose.
    """

    alias: str = Field(
        ...,
        description=(
            "The alternate name or ID to use. The alias does not have the restrictions "
            "that apply to name attributes. This is useful for capturing legacy "
            "identifiers for systems with unusual naming conventions. It is also "
            "useful for capturing variable names in software, amongst other things."
        ),
        examples=["BatteryVoltage", "BusBatteryVoltage", "BattVolt"],
    )
    """The alternate name or ID to use.

    The alias does not have the restrictions that apply to name attributes. This is
    useful for capturing legacy identifiers for systems with unusual naming conventions.
    It is also useful for capturing variable names in software, amongst other things.
    """


class AncillaryData(XtceBaseModel):
    """Use for any other data associated with a named item.

    May be used to include administrative data (e.g., version, CM or tags) or
    potentially any MIME type. Data may be included or given as an href.
    """

    value: str = Field(
        default="",
        description=(
            "The value of this Ancillary Data characteristic, feature, or data."
        ),
        examples=[
            "123 bytes",
            '{"min_size": 1, "max_size": 10}',
            "<SizeRange><MinSize>1</MinSize><MaxSize>10</MaxSize></SizeRange>",
        ],
    )
    """The value of this Ancillary Data characteristic, feature, or data."""

    name: str = Field(
        ...,
        description=(
            "Identifier for this Ancillary Data characteristic, feature, or data."
        ),
        examples=["ContainerSize", "SizeRangeDict", "SizeRangeXml"],
    )
    """Identifier for this Ancillary Data characteristic, feature, or data."""

    mime_type: str = Field(
        default="text/plain",
        description=(
            "Optional text encoding method for the element text content of this "
            "element."
        ),
        examples=["text/plain", "application/json", "application/xml"],
    )
    """Optional text encoding method for the element text content of this element."""

    href: str | None = Field(
        default=None,
        description=(
            "Optional Uniform Resource Identifier for this characteristic, "
            "feature, or data."
        ),
        examples=[
            "http://example.com/data",
            "https://example.com/data",
            "ftp://example.com/data",
        ],
    )
    """Optional Uniform Resource Identifier for this characteristic, feature, or
    data.
    """

class DescriptionBase(XtceBaseModel):
    """Defines an abstract schema type used as basis for NameDescriptionBase and
    OptionalNameDescriptionBase.
    """

    short_description: str | None = Field(
        default=None,
        description=(
            "Optional short description to be used for explanation of this item."
        ),
        max_length=80,
        examples=[
            "Battery voltage in volts",
            "The speed of RWA1 in m/s",
            "An unsigned 8-bit integer",
        ],
    )
    """Optional short description to be used for explanation of this item."""

    long_description: str | None = Field(
        default=None,
        description=(
            "Optional long form description to be used for explanatory descriptions of "
            "this item and may include HTML markup using CDATA. Long Descriptions are "
            "of unbounded length."
        ),
        examples=[
            (
                "This parameter represents the voltage of the battery in  volts. It is "
                "measured by the battery voltage sensor and is used to monitor the "
                "health of the battery."
            ),
            (
                "This parameter represents the speed of RWA1 in m/s. It is measured by "
                "the RWA1 speed sensor and is used to control RWA1."
            ),
            (
                "This parameter is an unsigned 8-bit integer. It is used to store "
                "small numerical values."
            ),
        ],
    )
    """Optional long form description to be used for explanatory descriptions of this
    item and may include HTML markup using CDATA.

    Long Descriptions are of unbounded length.
    """

    aliases: list[Alias] = Field(
        default_factory=list,
        min_length=1,
    )
    """Used to contain an alias (alternate) name or ID for this item."""

    ancillary_data: list[AncillaryData] = Field(
        default_factory=list,
        min_length=1,
    )
    """Use for any non-standard data associated with this named item."""

class NameDescriptionBase(DescriptionBase):
    """Defines a base schema type definition used by many other schema types throughout
    schema.
    """

    name: str = Field(
        ...,
        description="The name of this defined item.",
        pattern=r"^[^./:\[\] ]+$",
        examples=["BatteryVoltage", "setSpeed", "uint8"],
    )
    """The name of this defined item."""

class OptionalNameDescriptionBase(DescriptionBase):
    """The type definition used by most elements that have an optional name with
    optional descriptions.
    """
    name: str | None = Field(
        default=None,
        description="The optional name of this defined item.",
        pattern=r"^[^.\[\]:/ \t]+$",
        examples=["SpeedCommandVerifier", "LogMessageSet"],
    )
    """The optional name of this defined item."""
