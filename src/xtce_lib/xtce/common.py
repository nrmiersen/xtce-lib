"""Common base models."""

from abc import ABC
from typing import Annotated, Any, Self, assert_never

from pydantic import AfterValidator, Field

from xtce_lib.common.xtce_path import XtcePath, require_regex
from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from ._pattern import EXPD_NAME_REF_NO_PATH, EXPD_NAME_REF_W_PATH, NAME_REF_NO_PATH


class Alias(XtceBaseModel):
    """Used to contain an alternate name or ID for the object.

    For example, a parameter may have a mnemonic, an on-board id, and special IDs used
    by various ground software applications; all of these are aliases. Some ground
    system processing equipment has some severe naming restrictions on parameters (e.g.,
    names must be less than 12 characters, single case or integral id's only); their
    aliases provide a means of capturing each name in a "namespace". Note: the name is
    not reference-able (it cannot be used in a name reference substituting for the name
    of the item of interest).

    """

    namespace: str = Field(..., examples=["Bus", "Payload", "Ground"])
    """Aliases should be grouped together in a "namespace" so that they can be switched
    in and out of data extractions.

    The namespace generally identifies the purpose of the alternate name, whether for
    software variable names, additional operator names, or whatever the purpose.

    """

    alias: str = Field(
        ..., examples=["BatteryVoltage", "BusBatteryVoltage", "BattVolt"]
    )
    """The alternate name or ID to use.

    The alias does not have the restrictions that apply to name attributes. This is
    useful for capturing legacy identifiers for systems with unusual naming conventions.
    It is also useful for capturing variable names in software, amongst other things.

    """

    @classmethod
    def _from_v1_1(cls: type[Self], alias: xtce_1_1.AliasSetType.Alias) -> Self:
        return cls(namespace=alias.name_space, alias=alias.alias)

    @classmethod
    def _from_v1_2(cls: type[Self], alias: xtce_1_2.AliasType) -> Self:
        return cls(namespace=alias.name_space, alias=alias.alias)

    @classmethod
    def _from_v1_3(cls: type[Self], alias: xtce_1_3.AliasType) -> Self:
        return cls(namespace=alias.name_space, alias=alias.alias)

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create an Alias from an xsdata-generated AliasType object
        of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.AliasSetType.Alias:
        return xtce_1_1.AliasSetType.Alias(name_space=self.namespace, alias=self.alias)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AliasType:
        return xtce_1_2.AliasType(name_space=self.namespace, alias=self.alias)

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AliasType:
        return xtce_1_3.AliasType(name_space=self.namespace, alias=self.alias)

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.AliasSetType.Alias | xtce_1_2.AliasType | xtce_1_3.AliasType:
        """Convert this Alias to an xsdata-generated AliasType object of the specified
        version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class AncillaryData(XtceBaseModel):
    """Used for any other data associated with a named item.

    May be used to include administrative data (e.g., version, CM or tags) or
    potentially any MIME type. Data may be included or given as an href.

    """

    name: str = Field(..., examples=["ContainerSize", "SizeRangeDict", "SizeRangeXml"])
    """The identifier for this ancillary data."""

    value: str = Field(
        default="",
        examples=[
            "123 bytes",
            '{"min_size": 1, "max_size": 10}',
            "<SizeRange><MinSize>1</MinSize><MaxSize>10</MaxSize></SizeRange>",
        ],
    )
    """The value to store as ancillary data."""

    mime_type: str = Field(
        default="text/plain",
        examples=["text/plain", "application/json", "application/xml"],
    )
    """Optional text encoding method for the element text content of this element."""

    href: str | None = Field(
        default=None,
        examples=[
            "http://example.com/data",
            "https://example.com/data",
            "ftp://example.com/data",
        ],
    )
    """Optional Uniform Resource Identifier for this ancillary data."""

    @classmethod
    def _from_v1_1(
        cls: type[Self], alias: xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData
    ) -> Self:
        return cls(
            name=alias.name,
            value=alias.value,
            mime_type=alias.mime_type,
            href=alias.href,
        )

    @classmethod
    def _from_v1_2(cls: type[Self], alias: xtce_1_2.AncillaryDataType) -> Self:
        return cls(
            name=alias.name,
            value=alias.value,
            mime_type=alias.mime_type,
            href=alias.href,
        )

    @classmethod
    def _from_v1_3(cls: type[Self], alias: xtce_1_3.AncillaryDataType) -> Self:
        return cls(
            name=alias.name,
            value=alias.value,
            mime_type=alias.mime_type,
            href=alias.href,
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create an AncillaryData from an xsdata-generated
        AncillaryDataType object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData:
        return xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData(
            name=self.name, value=self.value, mime_type=self.mime_type, href=self.href
        )

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.AncillaryDataType:
        return xtce_1_2.AncillaryDataType(
            name=self.name, value=self.value, mime_type=self.mime_type, href=self.href
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.AncillaryDataType:
        return xtce_1_3.AncillaryDataType(
            name=self.name, value=self.value, mime_type=self.mime_type, href=self.href
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> (
        xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData
        | xtce_1_2.AncillaryDataType
        | xtce_1_3.AncillaryDataType
    ):
        """Convert this AncillaryData to an xsdata-generated AncillaryDataType object of
        the specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class DescriptionBase(XtceBaseModel, ABC):
    """An abstract schema type used as basis for NameDescriptionBase and
    OptionalNameDescriptionBase.
    """

    short_description: str | None = Field(
        default=None,
        max_length=80,
        examples=[
            "Battery voltage in volts",
            "The speed of RWA1 in m/s",
            "An unsigned 8-bit integer",
        ],
    )
    """Optional short description to be used for explanation of this element."""

    long_description: str | None = Field(
        default=None,
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
    element and may include HTML markup using CDATA.

    Long descriptions are of unbounded length.

    """

    aliases: list[Alias] = Field(default_factory=list, min_length=1)
    """Used to contain alternate names or IDs for the element."""

    ancillary_data: list[AncillaryData] = Field(default_factory=list, min_length=1)
    """Used to contain any ancillary data associated with the element."""


class NameDescriptionBase(DescriptionBase, ABC):
    """A base schema used by many other schema types throughout the schema."""

    name: str = Field(
        ...,
        pattern=r"^[^./:\[\] ]+$",
        examples=["BatteryVoltage", "setSpeed", "uint8"],
    )
    """The name of this element."""


class OptionalNameDescriptionBase(DescriptionBase, ABC):
    """A base schema used by most elements that have an optional name with optional
    descriptions.
    """

    name: str | None = Field(
        default=None,
        pattern=r"^[^.\[\]:/ \t]+$",
        examples=["SpeedCommandVerifier", "LogMessageSet"],
    )
    """The optional name of this element."""


class NameReferenceNoPath(XtceBaseModel, ABC):
    """A reference that can not include a path to a named element where array and
    aggregate are not possible.
    """

    name: str = Field(
        ...,
        pattern=NAME_REF_NO_PATH,
        examples=["Voltage"],
    )
    """A reference to a named element that can not include a path to the element.

    Can not include array or aggregate references.

    """


class ExpandedNameReferenceNoPath(XtceBaseModel, ABC):
    """A reference that can not include a path to a named element where array and
    aggregate are possible.
    """

    name: str = Field(
        ...,
        pattern=EXPD_NAME_REF_NO_PATH,
        examples=["Voltage[12].raw[3]"],
    )
    """A reference to a named element that can not include a path to the element.

    Can include array or aggregate references.

    """


class NameReferenceWithPath(XtceBaseModel, ABC):
    """A reference that can include a path to a named element where array and aggregate
    are not possible.
    """

    name: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[
                "/ConkSat/Bus/BatteryVoltage",
                "../Bus/BatteryVoltage",
                "../Payload/Camera/ExposureTime",
            ],
            json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
        )
    )
    """A Unix-like path to a parameter.

    Can not include array or aggregate references.

    """


class ExpandedNameReferenceWithPath(XtceBaseModel, ABC):
    """A reference that can include a path to a named element where array and aggregate
    are possible.
    """

    name: Annotated[XtcePath, AfterValidator(require_regex(EXPD_NAME_REF_W_PATH))] = (
        Field(
            ...,
            examples=[
                "ConkSat/Bus/Battery.voltage",
                "ConkSat/Bus/Battery[2].voltage",
                "ConkSat/Bus/BatteryVoltage[3]",
            ],
            json_schema_extra={"pattern": EXPD_NAME_REF_W_PATH},
        )
    )
    """A reference to a named element as a Unix style path to the element.

    Can include array and aggregate references.

    """
