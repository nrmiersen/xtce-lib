"""Array models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from pydantic import Field, model_validator
from typing_extensions import assert_never

from xtce_lib.common.xtce_version import XtceVersion
from xtce_lib.exceptions import DowngradePolicy, XtceUnsupportedError
from xtce_lib.generated import xtce_1_2, xtce_1_3

from ._base import XtceBaseModel
from .condition import ArgumentDiscreteLookupList, DiscreteLookupList

if TYPE_CHECKING:
    from .codec import ArgumentDynamicValue, DynamicValue


class Dimension(XtceBaseModel):
    """Used to define a subset of an array."""

    start_index: int | DynamicValue | DiscreteLookupList = Field(..., ge=0)
    """The start index of the array.

    Must be less than or equal to the end index.

    """

    end_index: int | DynamicValue | DiscreteLookupList = Field(..., ge=0)
    """The end index of the array.

    Must be greater than or equal to the start index.

    """

    @staticmethod
    def _resolve_index(value: int | DynamicValue | DiscreteLookupList) -> int | None:
        """Return an index value when validation is possible."""
        if isinstance(value, int):
            return value
        if isinstance(value, DiscreteLookupList):
            return value.default_value
        return None

    @model_validator(mode="after")
    def validate_indices(self) -> "Dimension":
        """Validate that the start index is less than or equal to the end index."""
        start_index = self._resolve_index(self.start_index)
        end_index = self._resolve_index(self.end_index)

        if start_index is None or end_index is None:
            # Cannot validate a dynamic value
            return self

        if start_index > end_index:
            raise ValueError(
                f"start index ({start_index}) must be less than or equal to end index ({end_index})"
            )

        return self

    @classmethod
    def _from_v1_2(cls: type[Self], dimension: xtce_1_2.DimensionType) -> Self:
        version = XtceVersion.V1_2

        def unpack_index(
            integer_value: xtce_1_2.IntegerValueType,
        ) -> int | DynamicValue | DiscreteLookupList:
            match integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list:
                case int():
                    return integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list
                case xtce_1_2.DynamicValueType():
                    return DynamicValue.from_xsdata(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list,
                        version,
                    )
                case xtce_1_2.DiscreteLookupListType():
                    return DiscreteLookupList.from_xsdata(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list
                    )

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    @classmethod
    def _from_v1_3(cls: type[Self], dimension: xtce_1_3.DimensionType) -> Self:
        version = XtceVersion.V1_3

        def unpack_index(
            integer_value: xtce_1_3.IntegerValueType,
        ) -> int | DynamicValue | DiscreteLookupList:
            match integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list:
                case int():
                    return integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list
                case xtce_1_3.DynamicValueType():
                    return DynamicValue.from_xsdata(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list,
                        version,
                    )
                case xtce_1_3.DiscreteLookupListType():
                    return DiscreteLookupList.from_xsdata(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list,
                        version,
                    )
                case None:
                    raise ValueError(
                        "invalid XTCE XML: dimension index is missing a value"
                    )
                case _:
                    assert_never(
                        integer_value.fixed_value_or_dynamic_value_or_discrete_lookup_list
                    )

        return cls(
            start_index=unpack_index(dimension.starting_index),
            end_index=unpack_index(dimension.ending_index),
        )

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a Dimension from an xsdata-generated Dimension
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, cls.__name__)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DimensionType:
        version = XtceVersion.V1_2

        def pack_index(
            value: int | DynamicValue | DiscreteLookupList,
        ) -> xtce_1_2.IntegerValueType:
            match value:
                case int():
                    return xtce_1_2.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value
                    )
                case DynamicValue():
                    return xtce_1_2.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value.to_xsdata(
                            version, policy
                        )
                    )
                case DiscreteLookupList():
                    return xtce_1_2.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value.to_xsdata(
                            version, policy
                        )
                    )

        return xtce_1_2.DimensionType(
            starting_index=xtce_1_2.IntegerValueType(
                fixed_value_or_dynamic_value_or_discrete_lookup_list=pack_index(
                    self.start_index
                )
            ),
            ending_index=xtce_1_2.IntegerValueType(
                fixed_value_or_dynamic_value_or_discrete_lookup_list=pack_index(
                    self.end_index
                )
            ),
        )

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DimensionType:
        version = XtceVersion.V1_3

        def pack_index(
            value: int | DynamicValue | DiscreteLookupList,
        ) -> xtce_1_3.IntegerValueType:
            match value:
                case int():
                    return xtce_1_3.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value
                    )
                case DynamicValue():
                    return xtce_1_3.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value.to_xsdata(
                            version, policy
                        )
                    )
                case DiscreteLookupList():
                    return xtce_1_3.IntegerValueType(
                        fixed_value_or_dynamic_value_or_discrete_lookup_list=value.to_xsdata(
                            version, policy
                        )
                    )

        return xtce_1_3.DimensionType(
            starting_index=xtce_1_3.IntegerValueType(
                fixed_value_or_dynamic_value_or_discrete_lookup_list=pack_index(
                    self.start_index
                )
            ),
            ending_index=xtce_1_3.IntegerValueType(
                fixed_value_or_dynamic_value_or_discrete_lookup_list=pack_index(
                    self.end_index
                )
            ),
        )

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DimensionType | xtce_1_3.DimensionType:
        """Convert this Dimension to an xsdata-generated Dimension object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                raise XtceUnsupportedError(version, self.__class__.__name__)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)


class ArgumentDimension(XtceBaseModel):
    start_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None,
        ge=0,
    )
    end_index: int | ArgumentDynamicValue | ArgumentDiscreteLookupList | None = Field(
        default=None,
        ge=0,
    )
