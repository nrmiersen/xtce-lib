"""Common base models."""

from abc import ABC
from typing import Any

from pydantic import Field

from xtce_lib.exceptions import DowngradePolicy
from xtce_lib.generated import xtce_1_1, xtce_1_2, xtce_1_3

from ._base import XtceBaseModel


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

    _v1_1_type = xtce_1_1.AliasSetType.Alias
    _v1_2_type = xtce_1_2.AliasType
    _v1_3_type = xtce_1_3.AliasType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.AliasSetType.Alias) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["namespace"] = obj.name_space
        kwargs["alias"] = obj.alias
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AliasType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["namespace"] = obj.name_space
        kwargs["alias"] = obj.alias
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AliasType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["namespace"] = obj.name_space
        kwargs["alias"] = obj.alias
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["name_space"] = self.namespace
        kwargs["alias"] = self.alias
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name_space"] = self.namespace
        kwargs["alias"] = self.alias
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name_space"] = self.namespace
        kwargs["alias"] = self.alias
        return kwargs


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

    _v1_1_type = xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData
    _v1_2_type = xtce_1_2.AncillaryDataType
    _v1_3_type = xtce_1_3.AncillaryDataType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.DescriptionType.AncillaryDataSet.AncillaryData
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["value"] = obj.value
        kwargs["mime_type"] = obj.mime_type
        kwargs["href"] = obj.href
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.AncillaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["value"] = obj.value
        kwargs["mime_type"] = obj.mime_type
        kwargs["href"] = obj.href
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.AncillaryDataType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        kwargs["value"] = obj.value
        kwargs["mime_type"] = obj.mime_type
        kwargs["href"] = obj.href
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["value"] = self.value
        kwargs["mime_type"] = self.mime_type
        kwargs["href"] = self.href
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["value"] = self.value
        kwargs["mime_type"] = self.mime_type
        kwargs["href"] = self.href
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        kwargs["value"] = self.value
        kwargs["mime_type"] = self.mime_type
        kwargs["href"] = self.href
        return kwargs


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

    aliases: list[Alias] = Field(default_factory=list)
    """Used to contain alternate names or IDs for the element."""

    ancillary_data: list[AncillaryData] = Field(default_factory=list)
    """Used to contain any ancillary data associated with the element."""

    _v1_1_type = xtce_1_1.DescriptionType
    _v1_2_type = xtce_1_2.DescriptionType
    _v1_3_type = xtce_1_3.DescriptionType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.DescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["short_description"] = obj.short_description
        kwargs["long_description"] = obj.long_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_1(data)
                for data in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set and obj.ancillary_data_set.ancillary_data
            else []
        )
        kwargs["aliases"] = (
            [Alias._from_v1_1(alias) for alias in obj.alias_set.alias]
            if obj.alias_set and obj.alias_set.alias
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.DescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["short_description"] = obj.short_description
        kwargs["long_description"] = obj.long_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_2(data)
                for data in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set and obj.ancillary_data_set.ancillary_data
            else []
        )
        kwargs["aliases"] = (
            [Alias._from_v1_2(alias) for alias in obj.alias_set.alias]
            if obj.alias_set and obj.alias_set.alias
            else []
        )
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.DescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["short_description"] = obj.short_description
        kwargs["long_description"] = obj.long_description
        kwargs["ancillary_data"] = (
            [
                AncillaryData._from_v1_3(data)
                for data in obj.ancillary_data_set.ancillary_data
            ]
            if obj.ancillary_data_set and obj.ancillary_data_set.ancillary_data
            else []
        )
        kwargs["aliases"] = (
            [Alias._from_v1_3(alias) for alias in obj.alias_set.alias]
            if obj.alias_set and obj.alias_set.alias
            else []
        )
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["short_description"] = self.short_description
        kwargs["long_description"] = self.long_description
        kwargs["ancillary_data_set"] = (
            xtce_1_1.DescriptionType.AncillaryDataSet(
                ancillary_data=[data._to_v1_1(policy) for data in self.ancillary_data]
            )
            if self.ancillary_data
            else None
        )
        kwargs["alias_set"] = (
            xtce_1_1.AliasSetType(
                alias=[alias._to_v1_1(policy) for alias in self.aliases]
            )
            if self.aliases
            else None
        )
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["short_description"] = self.short_description
        kwargs["long_description"] = self.long_description
        kwargs["ancillary_data_set"] = (
            xtce_1_2.AncillaryDataSetType(
                ancillary_data=[data._to_v1_2(policy) for data in self.ancillary_data]
            )
            if self.ancillary_data
            else None
        )
        kwargs["alias_set"] = (
            xtce_1_2.AliasSetType(
                alias=[alias._to_v1_2(policy) for alias in self.aliases]
            )
            if self.aliases
            else None
        )
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["short_description"] = self.short_description
        kwargs["long_description"] = self.long_description
        kwargs["ancillary_data_set"] = (
            xtce_1_3.AncillaryDataSetType(
                ancillary_data=[data._to_v1_3(policy) for data in self.ancillary_data]
            )
            if self.ancillary_data
            else None
        )
        kwargs["alias_set"] = (
            xtce_1_3.AliasSetType(
                alias=[alias._to_v1_3(policy) for alias in self.aliases]
            )
            if self.aliases
            else None
        )
        return kwargs


class NameDescriptionBase(DescriptionBase, ABC):
    """A base schema used by many other schema types throughout the schema."""

    name: str = Field(
        ...,
        pattern=r"^[^./:\[\] ]+$",
        examples=["BatteryVoltage", "setSpeed", "uint8"],
    )
    """The name of this element."""

    _v1_1_type = xtce_1_1.NameDescriptionType
    _v1_2_type = xtce_1_2.NameDescriptionType
    _v1_3_type = xtce_1_3.NameDescriptionType

    @classmethod
    def _from_v1_1_kwargs(cls, obj: xtce_1_1.NameDescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: xtce_1_2.NameDescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: xtce_1_3.NameDescriptionType) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs


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

    _v1_1_type = xtce_1_1.OptionalNameDescriptionType
    _v1_2_type = xtce_1_2.OptionalNameDescriptionType
    _v1_3_type = xtce_1_3.OptionalNameDescriptionType

    @classmethod
    def _from_v1_1_kwargs(
        cls, obj: xtce_1_1.OptionalNameDescriptionType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(
        cls, obj: xtce_1_2.OptionalNameDescriptionType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(
        cls, obj: xtce_1_3.OptionalNameDescriptionType
    ) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs
